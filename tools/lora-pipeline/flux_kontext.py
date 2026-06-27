#!/usr/bin/env python
"""FLUX.1 Kontext character-consistency route -- ONE route (SDXL bootstrap is a separate
script by design; see README). Kontext is an in-context EDIT model: it keeps the subject
of the reference image natively (no IPAdapter) and re-scenes / re-poses it per a natural
language instruction.

Config-driven: nothing about the model is hardcoded (unet / clip / vae / sampler /
instructions all live in config.flux.json). Shares ComfyUI transport with comfy_common.py.
Stdlib only.

    python flux_kontext.py --config config.flux.json --limit 1 --wait   # smoke test
    python flux_kontext.py --config config.flux.json --wait             # full matrix
"""
import argparse
import os
import sys

# ComfyUI's embedded Python (embeddable build) does not auto-add the script's own
# directory to sys.path, so make the sibling comfy_common import work regardless of
# how/where we are launched.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comfy_common as cc  # noqa: E402


def build_graph(cfg, instruction, seed, prefix, ref_names):
    """Build the Flux Kontext workflow (API format).

    Reference image -> FluxKontextImageScale -> VAEEncode -> ReferenceLatent embeds it
    into the conditioning (this is the Kontext mechanism). KSampler runs on the Kontext
    UNET at cfg=1 with a zeroed-out negative.
    """
    m = cfg["models"]
    k = cfg["kontext"]
    s = cfg["sampler"]
    cv = cfg.get("canvas", {})
    g = {
        "1": {"class_type": "UNETLoader",
              "inputs": {"unet_name": m["unet"], "weight_dtype": m.get("weight_dtype", "default")}},
        "2": {"class_type": "DualCLIPLoader",
              "inputs": {"clip_name1": m["clip_l"], "clip_name2": m["clip_t5"], "type": "flux"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": m["vae"]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": instruction}},
        "9": {"class_type": "FluxGuidance",
              "inputs": {"conditioning": ["7", 0], "guidance": k.get("guidance", 2.5)}},
        "10": {"class_type": "ConditioningZeroOut", "inputs": {"conditioning": ["7", 0]}},
        "12": {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": ["3", 0]}},
        "13": {"class_type": "SaveImage", "inputs": {"images": ["12", 0], "filename_prefix": prefix}},
    }
    # reference image(s): each -> scale -> encode -> chained ReferenceLatent into conditioning
    cond = ["7", 0]
    first_enc = None
    for i, rn in enumerate(ref_names):
        li, si, ei, ri = "4_%d" % i, "5_%d" % i, "6_%d" % i, "8_%d" % i
        g[li] = {"class_type": "LoadImage", "inputs": {"image": rn}}
        g[si] = {"class_type": "FluxKontextImageScale", "inputs": {"image": [li, 0]}}
        g[ei] = {"class_type": "VAEEncode", "inputs": {"pixels": [si, 0], "vae": ["3", 0]}}
        g[ri] = {"class_type": "ReferenceLatent", "inputs": {"conditioning": cond, "latent": [ei, 0]}}
        cond = [ri, 0]
        if first_enc is None:
            first_enc = [ei, 0]
    g["9"]["inputs"]["conditioning"] = cond
    # canvas (KSampler latent_image source):
    #   reference -> edit the reference latent (canonical, strongest preservation)
    #   empty     -> a blank latent of chosen size (more framing freedom; the variety lever)
    if cv.get("mode", "reference") == "empty":
        g["14"] = {"class_type": "EmptySD3LatentImage",
                   "inputs": {"width": cv.get("width", 832), "height": cv.get("height", 1216),
                              "batch_size": 1}}
        canvas_ref = ["14", 0]
    else:
        canvas_ref = first_enc
    # optional LoRA stack (model-only for Flux/Kontext: UNet side; most Flux LoRAs are
    # UNet-only). Empty list -> model_src stays ["1", 0] (graph identical to no-LoRA).
    loras = m.get("loras", [])
    model_src = ["1", 0]
    for i, lo in enumerate(loras):
        lid = "1L_%d" % i
        g[lid] = {"class_type": "LoraLoaderModelOnly",
                  "inputs": {"model": model_src, "lora_name": lo["name"],
                             "strength_model": lo.get("strength_model", 1.0)}}
        model_src = [lid, 0]
    g["11"] = {"class_type": "KSampler",
               "inputs": {"model": model_src, "positive": ["9", 0], "negative": ["10", 0],
                          "latent_image": canvas_ref, "seed": seed, "steps": s["steps"],
                          "cfg": s["cfg"], "sampler_name": s["sampler_name"],
                          "scheduler": s["scheduler"], "denoise": s.get("denoise", 1.0)}}
    return g


def iter_jobs(cfg):
    """Expand instruction_template x variations x seeds into (index, instruction, seed, prefix)."""
    p = cfg["prompt"]
    tmpl = p["instruction_template"]
    variations = p["variations"]
    seeds = cfg.get("seeds_per_prompt", 2)
    base = cfg.get("seed_base", 7000)
    prefix0 = cfg.get("output_prefix", "charkontext/img")
    n = 0
    for pass_i in range(seeds):
        for i, v in enumerate(variations):
            instruction = tmpl.format(variation=v)
            seed = base + pass_i * 4000 + i * 13
            yield n, instruction, seed, "%s_%03d" % (prefix0, n)
            n += 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.flux.json")
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
    for idx, instruction, seed, prefix in iter_jobs(cfg):
        if args.limit and idx >= args.limit:
            break
        try:
            cc.submit(url, build_graph(cfg, instruction, seed, prefix, refs), "flux-kontext")
            ok += 1
        except Exception as e:  # noqa: BLE001
            fail += 1
            print("FAIL %s: %s" % (prefix, e))
        n += 1

    print("submitted=%d ok=%d fail=%d" % (n, ok, fail))
    if args.wait:
        print("waiting for queue to drain (Flux is ~3x slower than SDXL)...")
        print("queue empty -- done." if cc.wait_for_drain(url, max_polls=600) else "timed out (jobs may still run).")


if __name__ == "__main__":
    main()
