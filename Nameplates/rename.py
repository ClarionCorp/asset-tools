import os
import re
import shutil

# Paths
uasset_folder = './uassets'
nameplates_folder = './nameplates'
linked_folder = './linked'

# Ensure the linked folder exists
os.makedirs(linked_folder, exist_ok=True)

# Regex (case-insensitive): matches optional subfolder and T_name_small
texture_pattern = re.compile(
    r'/Game/Prometheus/UI/OutOfGame/Personalization/Nameplates(?:/([^/]+))?/+(T_[^/\\]+?_small)',
    re.IGNORECASE
)

# Supported image extensions
image_extensions = ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tga']

# Process each .uasset file
for filename in os.listdir(uasset_folder):
    if not filename.endswith('.uasset'):
        continue

    uasset_path = os.path.join(uasset_folder, filename)
    uasset_name = os.path.splitext(filename)[0]

    try:
        with open(uasset_path, 'r', encoding='latin-1', errors='ignore') as file:
            content = file.read()
    except Exception as e:
        print(f"[ERROR] Failed to read {filename}: {e}")
        continue

    match = texture_pattern.search(content)
    if not match:
        print(f"[WARN] No match found in {filename}")
        continue

    subfolder, texture_name = match.groups()
    search_dirs = [nameplates_folder] if subfolder is None else [os.path.join(nameplates_folder, subfolder)]

    found = False
    for search_dir in search_dirs:
        for ext in image_extensions:
            source_path = os.path.join(search_dir, texture_name + ext)
            if os.path.exists(source_path):
                dest_filename = uasset_name + ext
                dest_path = os.path.join(linked_folder, dest_filename)
                shutil.move(source_path, dest_path)
                print(f"[OK] Moved and renamed: {texture_name + ext} → linked/{dest_filename}")
                found = True
                break
        if found:
            break

    if not found:
        print(f"[MISS] No image found for {texture_name} in {search_dirs[0]}")
