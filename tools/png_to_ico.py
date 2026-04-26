"""
png_to_ico.py — PNG 轉多尺寸 ICO,內建亮度去背

用途:
    把 ComfyUI 出的「黑底 + 發光主體」PNG 轉成透明背景多尺寸 ICO,
    用於 Windows 桌面捷徑 / taskbar 圖示。

使用:
    & "D:\\Work\\ComfyUI_portable\\ComfyUI_windows_portable\\python_embeded\\python.exe" `
      "D:\\Work\\system-setup\\tools\\png_to_ico.py" `
      "<input.png>" "<output.ico>"

可選參數:
    --no-bg-removal       不去背(直接原圖轉 ICO)
    --threshold-min N     亮度低於 N 完全透明(預設 20)
    --threshold-max N     亮度高於 N 完全不透明(預設 70)
    --sizes 16,24,32,...  自訂尺寸(預設 16,24,32,48,64,128,256)

範例:
    # 一般用法
    python png_to_ico.py input.png output.ico

    # 微調閾值(背景沒清乾淨時調高 min,主體被吃掉時調低 max)
    python png_to_ico.py input.png output.ico --threshold-min 30 --threshold-max 90

    # 完全不去背
    python png_to_ico.py input.png output.ico --no-bg-removal

依賴:
    Pillow(ComfyUI portable 已內建)

作者:Wayne system-setup
"""

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("[ERROR] Pillow 未安裝。請用 ComfyUI 內建 python:")
    print('  & "D:\\Work\\ComfyUI_portable\\ComfyUI_windows_portable\\python_embeded\\python.exe" -m pip install Pillow')
    sys.exit(1)


DEFAULT_SIZES = [16, 24, 32, 48, 64, 128, 256]


def luminance_based_alpha(img: Image.Image, threshold_min: int, threshold_max: int) -> Image.Image:
    """
    根據亮度生成 alpha channel:
        亮度 < threshold_min  → alpha = 0   (完全透明)
        亮度 > threshold_max  → alpha = 255 (完全不透明)
        中間漸變(平滑邊緣,避免毛邊)
    """
    img = img.convert("RGBA")
    pixels = img.load()
    w, h = img.size

    span = max(threshold_max - threshold_min, 1)

    for y in range(h):
        for x in range(w):
            r, g, b, _ = pixels[x, y]
            # ITU-R BT.601 亮度公式
            lum = 0.299 * r + 0.587 * g + 0.114 * b

            if lum <= threshold_min:
                alpha = 0
            elif lum >= threshold_max:
                alpha = 255
            else:
                alpha = int((lum - threshold_min) / span * 255)

            pixels[x, y] = (r, g, b, alpha)

    return img


def make_ico(input_path: Path, output_path: Path, sizes: list[int],
             remove_bg: bool, t_min: int, t_max: int) -> None:
    print(f"[INFO] 讀取:{input_path}")
    img = Image.open(input_path)
    print(f"[INFO] 原始尺寸:{img.size},模式:{img.mode}")

    if remove_bg:
        print(f"[INFO] 套用亮度去背(min={t_min}, max={t_max})...")
        img = luminance_based_alpha(img, t_min, t_max)
    else:
        img = img.convert("RGBA")
        print("[INFO] 跳過去背")

    # 確保是正方形(ICO 標準),不是的話置中裁切
    if img.width != img.height:
        print(f"[WARN] 非正方形({img.width}x{img.height}),置中裁切為正方形")
        side = min(img.width, img.height)
        left = (img.width - side) // 2
        top = (img.height - side) // 2
        img = img.crop((left, top, left + side, top + side))

    # 確認輸出資料夾存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 多尺寸寫進同一個 ICO
    print(f"[INFO] 輸出尺寸:{sizes}")
    img.save(
        output_path,
        format="ICO",
        sizes=[(s, s) for s in sizes],
    )
    print(f"[OK] 已輸出:{output_path}")
    print(f"     檔案大小:{output_path.stat().st_size / 1024:.1f} KB")


def parse_sizes(s: str) -> list[int]:
    try:
        sizes = [int(x.strip()) for x in s.split(",")]
        for v in sizes:
            if v < 8 or v > 256:
                raise ValueError(f"尺寸 {v} 超出合理範圍 (8-256)")
        return sizes
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))


def main():
    parser = argparse.ArgumentParser(
        description="PNG 轉多尺寸 ICO(內建亮度去背)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("input", type=Path, help="輸入 PNG 路徑")
    parser.add_argument("output", type=Path, help="輸出 ICO 路徑")
    parser.add_argument("--no-bg-removal", action="store_true", help="不去背")
    parser.add_argument("--threshold-min", type=int, default=20,
                        help="亮度低於此值完全透明(預設 20)")
    parser.add_argument("--threshold-max", type=int, default=70,
                        help="亮度高於此值完全不透明(預設 70)")
    parser.add_argument("--sizes", type=parse_sizes, default=DEFAULT_SIZES,
                        help="自訂尺寸,逗號分隔(預設 16,24,32,48,64,128,256)")

    args = parser.parse_args()

    if not args.input.exists():
        print(f"[ERROR] 輸入檔不存在:{args.input}")
        sys.exit(1)

    if args.threshold_min >= args.threshold_max:
        print("[ERROR] threshold-min 必須小於 threshold-max")
        sys.exit(1)

    make_ico(
        input_path=args.input,
        output_path=args.output,
        sizes=args.sizes,
        remove_bg=not args.no_bg_removal,
        t_min=args.threshold_min,
        t_max=args.threshold_max,
    )


if __name__ == "__main__":
    main()
