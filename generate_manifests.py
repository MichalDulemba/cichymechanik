#!/usr/bin/env python3
"""
generate_manifests.py
Uruchom z głównego folderu repozytorium:
  python generate_manifests.py

Skanuje graphics/build01/ ... build09/ i tworzy manifest.json
z listą wszystkich zdjęć w folderze.
Uruchamiaj za każdym razem gdy dodasz lub usuniesz zdjęcia.
"""

import os
import json
import glob

GRAPHICS_DIR = "graphics"
BUILD_FOLDERS = [f"build{i:02d}" for i in range(1, 10)]
IMAGE_EXTENSIONS = ("*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG", "*.webp", "*.WEBP")

def generate_manifest(folder_path):
    images = []
    for ext in IMAGE_EXTENSIONS:
        found = glob.glob(os.path.join(folder_path, ext))
        images.extend(found)

    # Sortuj numerycznie jeśli możliwe, inaczej alfabetycznie
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
        print(f"Błąd: folder '{GRAPHICS_DIR}' nie istnieje.")
        print("Uruchom skrypt z głównego folderu repozytorium.")
        return

    total = 0
    for build in BUILD_FOLDERS:
        folder_path = os.path.join(GRAPHICS_DIR, build)
        if not os.path.exists(folder_path):
            print(f"  {build}/  — brak folderu, pomijam")
            continue

        images = generate_manifest(folder_path)
        count = len(images)
        total += count

        if count == 0:
            print(f"  {build}/  — brak zdjęć (manifest.json pusty)")
        else:
            print(f"  {build}/  — {count} zdjęć: {', '.join(images)}")

    print(f"\nGotowe. Łącznie {total} zdjęć w {len(BUILD_FOLDERS)} folderach.")
    print("Wrzuć zmiany na GitHub — Cloudflare automatycznie wdroży.")

if __name__ == "__main__":
    main()
