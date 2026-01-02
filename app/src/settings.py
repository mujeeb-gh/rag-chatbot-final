import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


SRC_DIR: str = os.path.dirname(__file__)
DATA_DIR: str = os.path.join(SRC_DIR, "../../data")
CHROMA_DIR: str = os.path.join(SRC_DIR, "../../.chroma")
MODELS_DIR: str = os.path.join(SRC_DIR, "../../models")
CHROMA_COLLECTION: str = "bge_small_finetuned_astra_collection_10k"


class Settings(BaseSettings):
    cohere_api_key: str = ""
    groq_api_key: str = ""
    openai_api_key: str = ""
    openrouter_api_key: str = ""
    # HuggingFace Hub configuration
    hf_models_repo: str = os.getenv("HF_MODELS_REPO", "")
    hf_chromadb_repo: str = os.getenv("HF_CHROMADB_REPO", "")
    hf_token: str = os.getenv("HF_TOKEN", "")


settings = Settings()
