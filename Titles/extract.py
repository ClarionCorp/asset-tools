import os
import json

jsons_folder = './jsons'
output_file = 'output.ts'

# Container for output
titles = []

# Gather JSON files
for filename in os.listdir(jsons_folder):
    if not filename.endswith('.json'):
        continue

    filepath = os.path.join(jsons_folder, filename)
    id_name = os.path.splitext(filename)[0]

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to parse {filename}: {e}")
        continue

    if not isinstance(data, list) or len(data) == 0:
        print(f"[SKIP] {filename} is not a valid array or is empty")
        continue

    try:
        localized_string = data[0]['Properties']['Title']['LocalizedString']
        if not isinstance(localized_string, str):
            raise ValueError("Not a string")
    except Exception:
        print(f"[SKIP] {filename} missing Title.LocalizedString")
        continue

    titles.append({
        "id": id_name,
        "en": localized_string
    })

# Write to output.ts
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("export const titles = [\n")
    for entry in titles:
        safe_en = entry["en"].replace('"', '\\"')
        f.write(f'  {{ id: "{entry["id"]}", en: "{safe_en}" }},\n')
    f.write("];\n")

print(f"[DONE] Wrote {len(titles)} entries to {output_file}")
