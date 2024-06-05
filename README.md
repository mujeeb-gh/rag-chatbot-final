# Astra


## Setup
To setup this project locally, you need to have a `.env` file in the root directory with the following variables:




Then, install the dependencies:

With development dependencies:
```bash
pip install -r requirements.dev.txt
```

Without development dependencies:
```bash
pip install -r requirements.txt
```

```
astra
├─ .chroma
│  ├─ chroma.sqlite3
│  ├─ dc7b6404-7ded-4d69-99f3-f52281dcd3a5
│  │  ├─ data_level0.bin
│  │  ├─ header.bin
│  │  ├─ length.bin
│  │  └─ link_lists.bin
│  └─ ed364018-df08-4fec-9296-0669e97a7ab7
│     ├─ data_level0.bin
│     ├─ header.bin
│     ├─ length.bin
│     └─ link_lists.bin
├─ .gitignore
├─ .python-version
├─ app
│  ├─ ingest.py
│  ├─ main.py
│  ├─ src
│  │  ├─ astra.py
│  │  ├─ chroma.py
│  │  ├─ llm.py
│  │  ├─ sentence.py
│  │  ├─ settings.py
│  │  ├─ template.py
│  │  ├─ test.py
│  │  └─ __init__.py
│  └─ __init__.py
├─ data
│  └─ sub_chunk_kb_acl-100k.csv
├─ pyproject.toml
├─ README.md
├─ requirements.dev.txt
└─ requirements.txt

```