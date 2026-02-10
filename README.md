---
title: Astra
emoji: 📉
colorFrom: pink
colorTo: gray
sdk: docker
pinned: false
license: mit
short_description: Chatbot for Scholarly Research using RAG
---

# Astra


## Setup
To setup this project locally, you need to have a `.env` file in the root directory with the following variables:

.venv is the new virtual env

### Environment Variables

Required for API keys:
- `GROQ_API_KEY`: Your Groq API key (for LLM)
- `OPENAI_API_KEY`: Your OpenAI API key (optional, for OpenAI models)
- `COHERE_API_KEY`: Your Cohere API key (optional)

For Docker deployment with HuggingFace Hub:
- `HF_MODELS_REPO`: HuggingFace Hub repository for models (e.g., "username/astra-models")
- `HF_CHROMADB_REPO`: HuggingFace Hub repository for ChromaDB embeddings (e.g., "username/astra-chromadb")
- `HF_TOKEN`: HuggingFace Hub token (required for private repositories)

Then, install the dependencies:

With development dependencies:
```bash
pip install -r requirements.dev.txt
```

Without development dependencies:
```bash
pip install -r requirements.txt
```

## Docker Deployment

The Dockerfile is configured to automatically download models and ChromaDB embeddings from HuggingFace Hub at container startup.

### Setting up HuggingFace Hub

1. Create a HuggingFace account at https://huggingface.co/
2. Create repositories for your models and ChromaDB:
   - Create a repository for models (e.g., `your-username/astra-models`)
   - Upload your model directories (`bge-large_finetuned/`, `bge-small_finetuned/`) to this repository
   - Create a repository for ChromaDB (e.g., `your-username/astra-chromadb`)
   - Compress your `.chroma/` directory and upload it as `chromadb.tar.gz` or `chromadb.zip`

3. Set environment variables when running Docker:
   ```bash
   docker run -e HF_MODELS_REPO=your-username/astra-models \
              -e HF_CHROMADB_REPO=your-username/astra-chromadb \
              -e HF_TOKEN=your_hf_token \
              -e GROQ_API_KEY=your_groq_key \
              -p 8501:8501 your-image-name
   ```

   Or use a `.env` file with Docker Compose or `--env-file` flag.

### Local Development

For local development, you can place models and ChromaDB files in the local directories:
- Models go in `models/` directory
- ChromaDB goes in `.chroma/` directory

The code will automatically use local files if available, falling back to HuggingFace Hub if not found.

## Project Structure

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
docker build -t astra
docker run -p 7860:7860 astra 