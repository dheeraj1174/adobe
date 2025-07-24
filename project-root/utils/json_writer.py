import json
import os

def save_to_json(title, outline, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data = {
        "title": title,
        "outline": outline
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
