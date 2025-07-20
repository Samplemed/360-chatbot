# Conversor CSV para TXT – Chatbot S360

Este projeto tem como objetivo converter arquivos CSV contendo artigos em formato JSON para arquivos `.txt`, prontos para uso com modelos de linguagem (chatbots, treinamentos, análises, etc).

Você pode gerar:
- Um único arquivo compilado com todos os artigos (`modo compilado`)
- Um arquivo individual `.txt` por artigo (`modo individual`)

---

## 🗂 Estrutura do Projeto

```bash
json_txt_chatbot/
├── converter/
│   ├── csv_converter.py
│   ├── json_converter.py
│   └── utils.py
├── tests/
│   └── test_converter.py
├── main.py
├── requirements.txt
└── README.md

Requisitos
Python 3.10 ou superior

Nenhuma biblioteca externa é necessária

