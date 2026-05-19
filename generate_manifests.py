#!/usr/bin/env python3
"""
generate_manifests.py
Uruchom z glownego folderu repozytorium:
  python generate_manifests.py

Skanuje graphics/build01/ ... build14/ i tworzy manifest.json
z lista wszystkich zdjec w folderze.
Uruchamiaj za kazdym razem gdy dodasz lub usuniesz zdjecia.
"""

import os
import json
import glob

GRAPHICS_DIR = "graphics"
BUILD_FOLDERS = [f"build{i:02d}" for i in range(1, 15)]
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

def generate_manifest(folder_path):
    seen = set()
    images = []
    for entry in os.scandir(folder_path):
        if not entry.is_file():
            continue
        if entry.name.lower().endswith(IMAGE_EXTENSIONS):
            lower = entry.name.lower()
            if lower not in seen:
                seen.add(lower)
                images.append(entry.path)

    def sort_key(path):
        name = os.path.splitext(os.path.basename(path))[0]
        try:
            return (0, int(name))
        except ValueError:
            return (1, name.lower())

    images.sort(key=sort_key)
    image_names = [os.path.basename(f) for f in images]

    manifest = {"images": image_names}
    manifest_path = os.path.join(folder_path, "manifest.json")

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    return image_names

def main():
    if not os.path.exists(GRAPHICS_DIR):
        print(f"Blad: folder '{GRAPHICS_DIR}' nie istnieje.")
        print("Uruchom skrypt z glownego folderu repozytorium.")
        return

    total = 0
    for build in BUILD_FOLDERS:
        folder_path = os.path.join(GRAPHICS_DIR, build)
        if not os.path.exists(folder_path):
            print(f"  {build}/  -- brak folderu, pomijam")
            continue

        images = generate_manifest(folder_path)
        count = len(images)
        total += count

        if count == 0:
            print(f"  {build}/  -- brak zdjec (manifest.json pusty)")
        else:
            print(f"  {build}/  -- {count} zdjec: {', '.join(images)}")

    print(f"\nGotowe. Lacznie {total} zdjec w {len(BUILD_FOLDERS)} folderach.")
    print("Wrzuc zmiany na GitHub -- Cloudflare automatycznie wdrazy.")

if __name__ == "__main__":
    main()
