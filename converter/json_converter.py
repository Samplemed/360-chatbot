import json
import os
from converter.utils import sanitize_text, save_txt

def convert_json_to_txt(json_path, output_dir):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, list):
            for i, item in enumerate(data):
                lines = []
                for key, value in item.items():
                    if isinstance(value, list):
                        for v in value:
                            lines.append(f"{key}: {json.dumps(v, ensure_ascii=False)}")
                    else:
                        lines.append(f"{key}: {sanitize_text(value)}")
                content = "\n".join(lines)
                save_txt(content, output_dir, f"document_{i + 1}.txt")
        else:
            print("JSON precisa ser uma lista de objetos.")