#!/usr/bin/env python
"""Build a numbered contact sheet from a folder of generated PNGs, for fast curation.

Needs Pillow. ComfyUI's embedded Python already has it, so run it with that:
    D:\\Work\\ComfyUI_portable\\ComfyUI_windows_portable\\python_embeded\\python.exe \\
        make_contactsheet.py --dir "<comfy_output>\\charlora_batch" --cols 8

The number drawn on each cell is the trailing index of the filename, so you can map a
keep/drop list straight back to the files.
"""
import argparse
import glob
import math
import os

from PIL import Image, ImageDraw, ImageFont


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="folder of PNGs")
    ap.add_argument("--out", default="", help="output path (default: <dir>_contact.png)")
    ap.add_argument("--cols", type=int, default=8)
    ap.add_argument("--thumb", type=int, default=200, help="thumbnail width in px")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.dir, "*.png")))
    if not files:
        print("no PNGs in %s" % args.dir)
        return
    tw = args.thumb
    th = int(tw * 1216 / 832)  # SDXL portrait ratio; thumbnails letterbox anyway
    lab = 20
    cols = args.cols
    rows = math.ceil(len(files) / cols)
    sheet = Image.new("RGB", (cols * tw, rows * (th + lab)), (20, 20, 24))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except Exception:  # noqa: BLE001
        font = ImageFont.load_default()

    for idx, f in enumerate(files):
        col, row = idx % cols, idx // cols
        x, y = col * tw, row * (th + lab)
        try:
            im = Image.open(f).convert("RGB")
            im.thumbnail((tw - 2, th - 2))
            sheet.paste(im, (x, y + lab))
        except Exception as e:  # noqa: BLE001
            print("skip %s: %s" % (f, e))
        parts = os.path.splitext(os.path.basename(f))[0].split("_")
        num = next((p for p in parts if p.isdigit()), str(idx))
        draw.text((x + 3, y), num, fill=(255, 230, 0), font=font)

    out = args.out or (args.dir.rstrip("\\/") + "_contact.png")
    sheet.save(out)
    print("saved %s  (%dx%d, %d images)" % (out, sheet.width, sheet.height, len(files)))


if __name__ == "__main__":
    main()
