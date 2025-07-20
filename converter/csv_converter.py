import os
import json

def convert_csv_to_single_txt(input_csv_path: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "output.txt")

    with open(input_csv_path, "r", encoding="utf-8") as infile, open(output_path, "w", encoding="utf-8") as outfile:
        for line in infile:
            try:
                data = json.loads(line)
                nome = data.get("article_name_pt_br", "Sem título")
                texto = data.get("texto", "")
                outfile.write(f"{nome}\n{texto}\n\n")
            except json.JSONDecodeError:
                print("[AVISO] Linha ignorada (não é JSON)")

def convert_csv_to_multiple_txt(input_csv_path: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    with open(input_csv_path, "r", encoding="utf-8") as infile:
        for idx, line in enumerate(infile, 1):
            try:
                data = json.loads(line)
                nome = data.get("article_name_pt_br", f"artigo_{idx}").replace(" ", "_")
                texto = data.get("texto", "")
                file_path = os.path.join(output_dir, f"{nome}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"{nome}\n{texto}")
            except json.JSONDecodeError:
                print("[AVISO] Linha ignorada (não é JSON)")

__all__ = ["convert_csv_to_single_txt", "convert_csv_to_multiple_txt"]
