import csv
import json
import os
import sys
import re

def sanitize_filename(name):
    """Remove caracteres inválidos para nomes de arquivos no Windows"""
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    name = " ".join(name.split())
    return name[:100].strip()

def format_article(data):
    """Formata o dicionário JSON em texto plano estruturado"""
    lines = []
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key.upper()}:")
            for item in value:
                if isinstance(item, dict):
                    for sub_k, sub_v in item.items():
                        lines.append(f"  - {sub_k}: {sub_v}")
                else:
                    lines.append(f"  - {item}")
        else:
            lines.append(f"{key.upper()}: {value}")
    return "\n".join(lines)

def convert_csv_to_single_txt(csv_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "artigos_compilados.txt")

    with open(csv_path, "r", encoding="utf-8") as f, open(output_path, "w", encoding="utf-8") as out_f:
        reader = csv.reader(f)
        for i, row in enumerate(reader, 1):
            if not row:
                continue
            try:
                data = json.loads(row[0])
                article_text = format_article(data)
                out_f.write(f"\n=== ARTIGO {i} ===\n")
                out_f.write(article_text)
                out_f.write("\n\n")
            except json.JSONDecodeError:
                print(f"[AVISO] Linha {i} ignorada (não é JSON)")

def convert_csv_to_multiple_txt(csv_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader, 1):
            if not row:
                continue
            try:
                data = json.loads(row[0])
                raw_name = data.get('article_name_pt_br')
                if not isinstance(raw_name, str) or not raw_name.strip():
                    raw_name = f"artigo_{i}"
                safe_name = sanitize_filename(raw_name).replace(" ", "_")
                filename = f"{i:04d}_{safe_name}.txt"
                output_path = os.path.join(output_dir, filename)
                with open(output_path, "w", encoding="utf-8") as out_f:
                    out_f.write(format_article(data))
            except json.JSONDecodeError:
                print(f"[AVISO] Linha {i} ignorada (não é JSON)")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python main.py <arquivo_entrada.csv> <pasta_saida> <modo>")
        print("Modo pode ser 'compilado' para um único arquivo ou 'individual' para arquivos separados")
        sys.exit(1)

    csv_path = sys.argv[1]
    output_dir = sys.argv[2]
    mode = sys.argv[3].lower()

    if mode == "compilado":
        convert_csv_to_single_txt(csv_path, output_dir)
        print(f"[OK] Todos artigos foram compilados no arquivo: {os.path.join(output_dir, 'artigos_compilados.txt')}")
    elif mode == "individual":
        convert_csv_to_multiple_txt(csv_path, output_dir)
        print(f"[OK] Todos artigos individuais foram gerados na pasta: {output_dir}")
    else:
        print("Modo inválido. Use 'compilado' ou 'individual'.")
