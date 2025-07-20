import unittest
from main import convert_csv_to_txt_compiled, convert_csv_to_multiple_txt
import os
import shutil

class TestCSVConverter(unittest.TestCase):
    def setUp(self):
        self.test_csv = "tests/test_data.csv"
        self.output_dir = "tests/output"
        os.makedirs(self.output_dir, exist_ok=True)

        # Cria um CSV de teste com 2 linhas JSON válidas
        with open(self.test_csv, "w", encoding="utf-8") as f:
            f.write('{"article_id": "001", "article_name_pt_br": "Teste 1"}\n')
            f.write('{"article_id": "002", "article_name_pt_br": "Teste 2"}\n')

    def tearDown(self):
        shutil.rmtree(self.output_dir)
        os.remove(self.test_csv)

    def test_compiled_output(self):
        convert_csv_to_txt_compiled(self.test_csv, self.output_dir)
        output_file = os.path.join(self.output_dir, "artigos_compilados.txt")
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Teste 1", content)
            self.assertIn("Teste 2", content)

    def test_multiple_output(self):
        convert_csv_to_multiple_txt(self.test_csv, self.output_dir)
        files = os.listdir(self.output_dir)
        self.assertEqual(len(files), 2)
        self.assertTrue(any("001" in name for name in files))
        self.assertTrue(any("002" in name for name in files))

if __name__ == '__main__':
    unittest.main()
