import os

def sanitize_text(text):
    if isinstance(text, str):
        return text.replace('\n', ' ').strip()
    return str(text)

def save_txt(content, output_dir, filename):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, filename)
    print(f"[SALVANDO ARQUIVO] {file_path}")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content + '\n')