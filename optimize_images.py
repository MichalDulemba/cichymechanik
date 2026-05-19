#!/usr/bin/env python3
"""
optimize_images.py
Kompresuje JPEGi w podanych folderach buildów do docelowej jakości.
Nadpisuje oryginały (wcześniej zrób backup lub commituj przed użyciem).

Użycie:
  python optimize_images.py               # wszystkie buildy
  python optimize_images.py build10 build11 build12
"""

import os
import sys
import glob
from PIL import Image

GRAPHICS_DIR = "graphics"
QUALITY = 82
MAX_WIDTH = 1920

import argparse

def optimize(folder_path, quality=QUALITY):
    patterns = ["*.jpg", "*.JPG", "*.jpeg", "*.JPEG"]
    files = []
    for p in patterns:
        files.extend(glob.glob(os.path.join(folder_path, p)))
    files = sorted(set(files))

    if not files:
        print(f"  {os.path.basename(folder_path)}/  -- brak JPEGow, pomijam")
        return

    saved_total = 0
    for fpath in files:
        before = os.path.getsize(fpath)
        img = Image.open(fpath).convert("RGB")
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            img = img.resize((MAX_WIDTH, int(img.height * ratio)), Image.LANCZOS)
        img.save(fpath, "JPEG", quality=quality, optimize=True)
        after = os.path.getsize(fpath)
        saved = before - after
        saved_total += saved
        name = os.path.basename(fpath)
        print(f"    {name}  {before//1024} KB -> {after//1024} KB  ({saved//1024:+} KB)")

    print(f"  SUM {os.path.basename(folder_path)}/  zaoszczedzono {saved_total//1024} KB\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('builds', nargs='*')
    parser.add_argument('--quality', type=int, default=QUALITY)
    args = parser.parse_args()

    if not os.path.exists(GRAPHICS_DIR):
        print("Blad: folder 'graphics' nie istnieje. Uruchom z glownego folderu repo.")
        return

    quality = args.quality
    if args.builds:
        builds = args.builds
    else:
        builds = sorted(os.listdir(GRAPHICS_DIR))
        builds = [b for b in builds if b.startswith("build")]

    for build in builds:
        folder_path = os.path.join(GRAPHICS_DIR, build)
        if not os.path.isdir(folder_path):
            print(f"  {build}/  — brak folderu")
            continue
        optimize(folder_path, quality)

    print("Gotowe.")

if __name__ == "__main__":
    main()
