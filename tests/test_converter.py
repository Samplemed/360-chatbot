import os
import shutil
import unittest

from converter.csv_converter import convert_csv_to_single_txt, convert_csv_to_multiple_txt

class TestCSVConverter(unittest.TestCase):
    def setUp(self):
        self.test_dir = "tests"
        self.test_csv = os.path.join(self.test_dir, "test_input.csv")
        self.output_dir = os.path.join(self.test_dir, "output")

        os.makedirs(self.test_dir, exist_ok=True)

        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        os.makedirs(self.output_dir, exist_ok=True)

        with open(self.test_csv, "w", encoding="utf-8") as f:
            f.write('{"article_name_pt_br": "Artigo 1", "texto": "Texto do primeiro artigo"}\n')
            f.write('{"article_name_pt_br": "Artigo 2", "texto": "Texto do segundo artigo"}\n')

    def tearDown(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)

    def test_single_txt_output(self):
        convert_csv_to_single_txt(self.test_csv, self.output_dir)
        output_path = os.path.join(self.output_dir, "output.txt")
        self.assertTrue(os.path.exists(output_path), "Arquivo compilado não foi criado.")

        with open(output_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Artigo 1", content)
            self.assertIn("Texto do segundo artigo", content)

    def test_multiple_output(self):
        convert_csv_to_multiple_txt(self.test_csv, self.output_dir)
        files = os.listdir(self.output_dir)
        print("Arquivos gerados:", files)
        self.assertEqual(len(files), 2, "Número incorreto de arquivos individuais gerados.")

        contents = []
        for file in files:
            path = os.path.join(self.output_dir, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                print(f"Conteúdo de {file}:\n{content}\n---")
                contents.append(content)

        self.assertTrue(any("Artigo_1" in c for c in contents), "Conteúdo 'Artigo_1' não encontrado em nenhum arquivo")
        self.assertTrue(any("Artigo_2" in c for c in contents), "Conteúdo 'Artigo_2' não encontrado em nenhum arquivo")

if __name__ == '__main__':
    unittest.main()
