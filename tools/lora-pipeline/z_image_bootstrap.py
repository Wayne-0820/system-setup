#!/usr/bin/env python
"""Z-Image Turbo (Moody Pro Mix) i2i "wash" bootstrap -- ONE route (SDXL/Flux are
separate scripts by design; see README). Z-Image has NO IPAdapter/Kontext identity
mechanism, so this is image-to-image variation: take a reference, re-noise it at a
moderate denoise, and let the model + seed re-roll lighting/framing/style. At cfg=1
(Turbo) the prompt has almost no guidance -- `denoise` is the similarity<->variation
lever. This is a "wash / variation" generator, NOT a character-consistency tool.

Config-driven: nothing about the model is hardcoded (checkpoint / clip / vae / sampler
/ denoise / shift / prompt all live in config.zimage.json). Shares ComfyUI transport
with comfy_common.py. Stdlib only.

    python z_image_bootstrap.py --config config.zimage.json --limit 1 --wait   # smoke
    python z_image_bootstrap.py --config config.zimage.json --wait             # full
"""
import argparse
import os
import sys

# ComfyUI's embedded Python does not auto-add the script's own directory to sys.path,
# so make the sibling comfy_common import work regardless of how we are launched.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comfy_common as cc  # noqa: E402


def build_graph(cfg, positive, negative, seed, prefix, ref_name):
    """Build the Z-Image i2i workflow (API format). ONE reference image per graph
    (one-job-per-ref): LoadImage -> scale to a sane size -> VAEEncode -> KSampler's
    latent_image (i2i). ModelSamplingAuraFlow patches the model (load-bearing for the
    Z-Image schedule). cfg=1, res_multistep/simple, denoise from config."""
    m = cfg["models"]
    s = cfg["sampler"]
    g = {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": m["checkpoint"]}},
        "2": {"class_type": "CLIPLoader",
              "inputs": {"clip_name": m["clip"], "type": m.get("clip_type", "lumina2")}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": m["vae"]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": positive}},
        "8": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": negative}},
        "5": {"class_type": "LoadImage", "inputs": {"image": ref_name}},
        "6": {"class_type": "ImageScaleToTotalPixels",
              "inputs": {"image": ["5", 0], "upscale_method": "lanczos",
                         "megapixels": s.get("target_megapixels", 1.0),
                         "resolution_steps": s.get("resolution_steps", 16)}},
        "9": {"class_type": "VAEEncode", "inputs": {"pixels": ["6", 0], "vae": ["3", 0]}},
        "12": {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": ["3", 0]}},
        "13": {"class_type": "SaveImage", "inputs": {"images": ["12", 0], "filename_prefix": prefix}},
    }
    # optional LoRA stack: checkpoint MODEL/CLIP -> chained LoraLoader(s) -> consumers
    # (ModelSamplingAuraFlow on model, CLIPTextEncode on clip). Empty list -> no-op.
    loras = m.get("loras", [])
    model_src, clip_src = ["1", 0], ["2", 0]
    for i, lo in enumerate(loras):
        lid = "1L_%d" % i
        g[lid] = {"class_type": "LoraLoader",
                  "inputs": {"model": model_src, "clip": clip_src,
                             "lora_name": lo["name"],
                             "strength_model": lo.get("strength_model", 1.0),
                             "strength_clip": lo.get("strength_clip", 1.0)}}
        model_src, clip_src = [lid, 0], [lid, 1]
    g["7"]["inputs"]["clip"] = clip_src
    g["8"]["inputs"]["clip"] = clip_src
    g["4"] = {"class_type": "ModelSamplingAuraFlow",
              "inputs": {"model": model_src, "shift": s.get("shift", 3.0)}}
    g["11"] = {"class_type": "KSampler",
               "inputs": {"model": ["4", 0], "positive": ["7", 0], "negative": ["8", 0],
                          "latent_image": ["9", 0], "seed": seed, "steps": s["steps"],
                          "cfg": s["cfg"], "sampler_name": s["sampler_name"],
                          "scheduler": s["scheduler"], "denoise": s.get("denoise", 0.55)}}
    return g


def iter_jobs(cfg, ref_names):
    """one-job-per-ref: expand refs x variations x seeds into
    (index, ref_name, positive, negative, seed, prefix)."""
    p = cfg["prompt"]
    idcore, neg = p["id_core"], p["negative"]
    variations = p["variations"]
    seeds = cfg.get("seeds_per_prompt", 2)
    base = cfg.get("seed_base", 9000)
    prefix0 = cfg.get("output_prefix", "zimage_batch/img")
    n = 0
    for ref in ref_names:
        for pass_i in range(seeds):
            for i, v in enumerate(variations):
                positive = "%s, %s" % (idcore, v)
                seed = base + pass_i * 4000 + i * 13
                yield n, ref, positive, neg, seed, "%s_%03d" % (prefix0, n)
                n += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.zimage.json")
    ap.add_argument("--limit", type=int, default=0, help="cap number of jobs (smoke test)")
    ap.add_argument("--wait", action="store_true", help="poll until the queue drains")
    args = ap.parse_args()

    cfg = cc.load_config(args.config)
    url = cfg.get("comfyui_url", "http://127.0.0.1:8188")
    refs = cc.stage_references(cfg["reference_image"], cfg.get("comfyui_input_dir"))
    if not refs:
        print("no reference image in config")
        return
    print("references staged: %s" % ", ".join(refs))

    n = ok = fail = 0
    for idx, ref, pos, neg, seed, prefix in iter_jobs(cfg, refs):
        if args.limit and idx >= args.limit:
            break
        try:
            cc.submit(url, build_graph(cfg, pos, neg, seed, prefix, ref), "z-image")
            ok += 1
        except Exception as e:  # noqa: BLE001
            fail += 1
            print("FAIL %s: %s" % (prefix, e))
        n += 1

    print("submitted=%d ok=%d fail=%d" % (n, ok, fail))
    if args.wait:
        print("waiting for queue to drain...")
        print("queue empty -- done." if cc.wait_for_drain(url, max_polls=600) else "timed out (jobs may still run).")


if __name__ == "__main__":
    main()
