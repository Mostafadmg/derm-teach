#!/usr/bin/env python3
"""Import a generated AI illustration: keep the untouched original in tools/v3/ai-src/, write a
white-trimmed, optimised copy to assets/img/ai/<name>.jpg.   Usage: import_ai.py <src.jpg> <name> [...]"""
import shutil, sys
from pathlib import Path
from PIL import Image, ImageChops
ROOT = Path(__file__).resolve().parents[2]
args = sys.argv[1:]
for src, name in zip(args[::2], args[1::2]):
    (ROOT / "tools/v3/ai-src").mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, ROOT / f"tools/v3/ai-src/{name}.jpg")
    im = Image.open(src).convert("RGB")
    diff = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).convert("L").point(lambda p: 255 if p > 22 else 0)
    x0, y0, x1, y1 = diff.getbbox()
    pad = int(0.05 * max(x1 - x0, y1 - y0))
    im = im.crop((max(0, x0 - pad), max(0, y0 - pad), min(im.width, x1 + pad), min(im.height, y1 + pad)))
    im.save(ROOT / f"assets/img/ai/{name}.jpg", quality=86, optimize=True, progressive=True)
    print(name, im.size)
