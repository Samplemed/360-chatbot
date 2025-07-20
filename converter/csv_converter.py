import json
import os

def convert_csv_to_txt(csv_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with open(csv_path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            # Remove as aspas duplas extremas se existirem
            if line.startswith('"') and line.endswith('"'):
                line = line[1:-1]

            # Substitui aspas duplas internas por aspas simples para formar JSON válido
            line = line.replace('""', '"')

            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                print(f"[ERRO] JSON inválido na linha {i}")
                continue

            # Monta texto de saída
            lines_out = []
            for key, value in data.items():
                if isinstance(value, list):
                    for v in value:
                        lines_out.append(f"{key}: {json.dumps(v, ensure_ascii=False)}")
                else:
                    lines_out.append(f"{key}: {value}")

            content = "\n".join(lines_out)

            output_file = os.path.join(output_dir, f"document_{i}.txt")
            with open(output_file, "w", encoding="utf-8") as out_f:
                out_f.write(content + "\n")

            print(f"[OK] Linha {i} processada e salva em {output_file}")
