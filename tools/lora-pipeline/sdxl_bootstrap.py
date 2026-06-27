#!/usr/bin/env python
"""SDXL IPAdapter character-LoRA bootstrap -- ONE route (Flux/Kontext is a separate
script by design; see README). Config-driven: nothing about the model is hardcoded
(checkpoint / vae / ipadapter / sampler / prompt matrix all live in the config JSON).
Swap any SDXL/Illustrious checkpoint by editing config.sdxl.json.

Shares ComfyUI transport with comfy_common.py. Stdlib only.

    python sdxl_bootstrap.py --config config.sdxl.json --limit 1 --wait   # smoke test
    python sdxl_bootstrap.py --config config.sdxl.json --wait             # full matrix
"""
import argparse
import os
import sys

# ComfyUI's embedded Python (embeddable build) does not auto-add the script's own
# directory to sys.path, so make the sibling comfy_common import work regardless of
# how/where we are launched.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comfy_common as cc  # noqa: E402


def build_graph(cfg, positive, negative, seed, prefix, ref_names):
    """Build the SDXL + IPAdapter PLUS workflow (API format). ref_names is a list of
    one or more reference filenames (batched into the IPAdapter for a stronger anchor)."""
    m = cfg["models"]
    ip = cfg["ipadapter"]
    s = cfg["sampler"]
    g = {
        "4": {"class_type": "CheckpointLoaderSimple",
              "inputs": {"ckpt_name": m["checkpoint"]}},
        "5": {"class_type": "IPAdapterUnifiedLoader",
              "inputs": {"model": ["4", 0],
                         "preset": m.get("ipadapter_preset", "PLUS (high strength)")}},
        "7": {"class_type": "IPAdapterAdvanced",
              "inputs": {"model": ["5", 0], "ipadapter": ["5", 1],
                         "weight": ip["weight"], "weight_type": ip["weight_type"],
                         "combine_embeds": ip.get("combine_embeds", "concat"),
                         "start_at": ip.get("start_at", 0.0),
                         "end_at": ip.get("end_at", 1.0),
                         "embeds_scaling": ip.get("embeds_scaling", "V only")}},
        "8": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 1], "text": positive}},
        "9": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 1], "text": negative}},
        "10": {"class_type": "EmptyLatentImage",
               "inputs": {"width": s["width"], "height": s["height"], "batch_size": 1}},
        "11": {"class_type": "KSampler",
               "inputs": {"model": ["7", 0], "positive": ["8", 0], "negative": ["9", 0],
                          "latent_image": ["10", 0], "seed": seed, "steps": s["steps"],
                          "cfg": s["cfg"], "sampler_name": s["sampler_name"],
                          "scheduler": s["scheduler"], "denoise": s.get("denoise", 1.0)}},
    }
    # optional LoRA stack: checkpoint MODEL/CLIP -> chained LoraLoader(s) -> consumers.
    # Applied BEFORE IPAdapter (IPAdapterUnifiedLoader still detects is_sdxl from the
    # model class). Empty list -> the repoints below are no-ops (graph identical).
    loras = m.get("loras", [])
    model_src, clip_src = ["4", 0], ["4", 1]
    for i, lo in enumerate(loras):
        lid = "4L_%d" % i
        g[lid] = {"class_type": "LoraLoader",
                  "inputs": {"model": model_src, "clip": clip_src,
                             "lora_name": lo["name"],
                             "strength_model": lo.get("strength_model", 1.0),
                             "strength_clip": lo.get("strength_clip", 1.0)}}
        model_src, clip_src = [lid, 0], [lid, 1]
    g["5"]["inputs"]["model"] = model_src
    g["8"]["inputs"]["clip"] = clip_src
    g["9"]["inputs"]["clip"] = clip_src
    # reference image(s): load each, batch them, feed the batch to the IPAdapter
    img_refs = []
    for i, rn in enumerate(ref_names):
        nid = "6_%d" % i
        g[nid] = {"class_type": "LoadImage", "inputs": {"image": rn}}
        img_refs.append([nid, 0])
    src = img_refs[0]
    for i in range(1, len(img_refs)):
        bid = "6b_%d" % i
        g[bid] = {"class_type": "ImageBatch", "inputs": {"image1": src, "image2": img_refs[i]}}
        src = [bid, 0]
    g["7"]["inputs"]["image"] = src
    vae = (m.get("vae") or "").strip()
    if vae:
        g["14"] = {"class_type": "VAELoader", "inputs": {"vae_name": vae}}
        vae_ref = ["14", 0]
    else:
        vae_ref = ["4", 2]
    g["12"] = {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": vae_ref}}
    g["13"] = {"class_type": "SaveImage", "inputs": {"images": ["12", 0], "filename_prefix": prefix}}
    return g


def iter_jobs(cfg):
    """Expand the prompt matrix into (index, positive, negative, seed, prefix) jobs."""
    p = cfg["prompt"]
    poses, scenes, outfits = p["poses"], p["scenes"], p["outfits"]
    idcore, neg = p["id_core"], p["negative"]
    seeds = cfg.get("seeds_per_prompt", 2)
    base = cfg.get("seed_base", 5000)
    prefix0 = cfg.get("output_prefix", "charlora_batch/img")
    n = 0
    for pass_i in range(seeds):
        for i, pose in enumerate(poses):
            outfit = outfits[(i + pass_i) % len(outfits)]
            scene = scenes[(i + pass_i) % len(scenes)]
            positive = "%s, %s, %s, %s" % (idcore, outfit, pose, scene)
            seed = base + pass_i * 4000 + i * 13
            yield n, positive, neg, seed, "%s_%03d" % (prefix0, n)
            n += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.sdxl.json")
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
    for idx, pos, neg, seed, prefix in iter_jobs(cfg):
        if args.limit and idx >= args.limit:
            break
        try:
            cc.submit(url, build_graph(cfg, pos, neg, seed, prefix, refs), "sdxl-bootstrap")
            ok += 1
        except Exception as e:  # noqa: BLE001
            fail += 1
            print("FAIL %s: %s" % (prefix, e))
        n += 1

    print("submitted=%d ok=%d fail=%d" % (n, ok, fail))
    if args.wait:
        print("waiting for queue to drain...")
        print("queue empty -- done." if cc.wait_for_drain(url) else "timed out (jobs may still run).")


if __name__ == "__main__":
    main()
