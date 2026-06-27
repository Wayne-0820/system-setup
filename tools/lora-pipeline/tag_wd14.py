#!/usr/bin/env python
"""WD14 tagger -> Danbooru-tag captions for a LoRA training dataset.

Standalone (does NOT drive ComfyUI): runs a WD14 ONNX tagger via onnxruntime, which is
already in ComfyUI's embedded Python -> no new deps, no ComfyUI node. For each image in
dataset_dir it writes a sibling .txt caption:

    <trigger_word>, <danbooru tags...>

with the config `strip_tags` (the character's intrinsic appearance) removed, so those
features bake into the trigger word instead of staying prompt-controllable.

Shares only `comfy_common.load_config` (tagging is not a ComfyUI generation job).

Run with ComfyUI's embedded python (has onnxruntime / PIL / numpy):
    <embedded_python> tag_wd14.py --config config.tagger.json
    <embedded_python> tag_wd14.py --config config.tagger.json --smoke <one_image>
"""
import argparse
import csv
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import comfy_common as cc  # noqa: E402


def _setup_cuda_dlls():
    """Let onnxruntime's CUDA EP find its CUDA 12 runtime DLLs. The portable's torch
    ships CUDA 13 (cublasLt64_13 etc.), but onnxruntime needs the CUDA 12 math libs
    (cublasLt64_12, cufft64_11, ...), so we point it at an isolated CUDA-12 dir
    (installed once via `pip install --target=<dir> nvidia-cublas-cu12 nvidia-cufft-cu12
    nvidia-curand-cu12 nvidia-cusolver-cu12 nvidia-cusparse-cu12 nvidia-cuda-runtime-cu12`)
    plus torch's own lib dir (which has cuDNN 9). MUST run before `import onnxruntime`.
    No-op if the dir is absent -> the session falls back to CPU. Override via
    $WD14_CUDA_LIBS. This only affects this tagging subprocess, not ComfyUI itself."""
    import glob

    dirs = sorted(glob.glob(os.path.join(
        os.environ.get("WD14_CUDA_LIBS", r"D:\Models\wd14\_onnxgpu_cu12"), "nvidia", "*", "bin")))
    try:
        import torch

        dirs.append(os.path.join(os.path.dirname(torch.__file__), "lib"))
    except Exception:  # noqa: BLE001
        pass
    dirs = [d for d in dirs if os.path.isdir(d)]
    if dirs:
        os.environ["PATH"] = os.pathsep.join(dirs) + os.pathsep + os.environ.get("PATH", "")
        for d in dirs:
            try:
                os.add_dll_directory(d)
            except Exception:  # noqa: BLE001
                pass


_setup_cuda_dlls()

import numpy as np  # noqa: E402
import onnxruntime as ort  # noqa: E402
from PIL import Image  # noqa: E402

HF = "https://huggingface.co/%s/resolve/main/%s"


def ensure_model(repo, model_dir):
    """Download model.onnx + selected_tags.csv from the HF repo if not already present."""
    os.makedirs(model_dir, exist_ok=True)
    onnx = os.path.join(model_dir, "model.onnx")
    csvp = os.path.join(model_dir, "selected_tags.csv")
    for name, path in (("selected_tags.csv", csvp), ("model.onnx", onnx)):
        if not os.path.exists(path) or os.path.getsize(path) < 1024:
            print("downloading %s (one-time)..." % name)
            urllib.request.urlretrieve(HF % (repo, name), path)
    return onnx, csvp


def load_tags(csvp):
    names, cats = [], []
    with open(csvp, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            names.append(row["name"])
            cats.append(int(row["category"]))
    return names, cats


def preprocess(path, size):
    """SmilingWolf WD14 preprocessing: pad to square (white), resize, RGB->BGR, float32."""
    img = Image.open(path).convert("RGB")
    w, h = img.size
    m = max(w, h)
    canvas = Image.new("RGB", (m, m), (255, 255, 255))
    canvas.paste(img, ((m - w) // 2, (m - h) // 2))
    canvas = canvas.resize((size, size), Image.BICUBIC)
    arr = np.asarray(canvas, dtype=np.float32)[:, :, ::-1]  # RGB -> BGR
    return np.expand_dims(arr, axis=0)


def caption_for(path, sess, in_name, size, names, cats, cfg):
    t = cfg["tagger"]
    probs = sess.run(None, {in_name: preprocess(path, size)})[0][0]
    gen_th = t.get("general_threshold", 0.35)
    chr_th = t.get("character_threshold", 0.85)
    picked = []
    for i, p in enumerate(probs):
        c = cats[i]
        if (c == 0 and p >= gen_th) or (c == 4 and p >= chr_th):
            picked.append((names[i], float(p)))
        elif c == 9 and t.get("include_rating", False) and p >= 0.5:
            picked.append((names[i], float(p)))
    if cfg.get("sort_by_confidence", True):
        picked.sort(key=lambda x: x[1], reverse=True)
    out = [n for n, _ in picked]
    if cfg.get("underscores_to_spaces", True):
        out = [n.replace("_", " ") for n in out]
    strip = set(s.lower() for s in cfg.get("strip_tags", []))
    out = [n for n in out if n.lower() not in strip]
    trig = (cfg.get("trigger_word") or "").strip()
    if trig:
        out = [trig] + out
    return ", ".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.tagger.json")
    ap.add_argument("--smoke", default="", help="tag ONE image, print result, write nothing")
    args = ap.parse_args()

    cfg = cc.load_config(args.config)
    t = cfg["tagger"]
    onnx, csvp = ensure_model(t["model_repo"], t["model_dir"])
    names, cats = load_tags(csvp)
    sess = ort.InferenceSession(onnx, providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
    in_name = sess.get_inputs()[0].name
    size = sess.get_inputs()[0].shape[1]
    size = size if isinstance(size, int) else 448
    print("model ready (input %dx%d, %d tags, providers=%s)" % (size, size, len(names), sess.get_providers()))

    if args.smoke:
        print("--- %s ---" % os.path.basename(args.smoke))
        print(caption_for(args.smoke, sess, in_name, size, names, cats, cfg))
        return

    ddir = cfg.get("dataset_dir", "")
    if not ddir or not os.path.isdir(ddir):
        print("dataset_dir not set or missing: %r -- set it in the config." % ddir)
        return
    exts = tuple(e.lower() for e in cfg.get("image_exts", [".png", ".jpg", ".jpeg", ".webp"]))
    imgs = [f for f in sorted(os.listdir(ddir)) if f.lower().endswith(exts)]
    done = 0
    for f in imgs:
        ip = os.path.join(ddir, f)
        txt = os.path.splitext(ip)[0] + ".txt"
        if os.path.exists(txt) and not cfg.get("overwrite_existing", True):
            continue
        cap = caption_for(ip, sess, in_name, size, names, cats, cfg)
        with open(txt, "w", encoding="utf-8") as fp:
            fp.write(cap)
        done += 1
        print("[%d/%d] %s" % (done, len(imgs), f))
    print("tagged %d / %d images in %s" % (done, len(imgs), ddir))


if __name__ == "__main__":
    main()
