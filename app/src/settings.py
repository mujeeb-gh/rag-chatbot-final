import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


class Settings(BaseSettings):
    cohere_api_key: str = ""
    groq_api_key: str = ""
    openai_api_key: str = ""
    openrouter_api_key: str = ""
    # HuggingFace Hub configuration
    hf_token: str = os.getenv("HF_TOKEN", "")
    
    chroma_db: str = os.getenv("CHROMA_DB", "bge-small-finetuned-chroma")
    chroma_collection: str = os.getenv("CHROMA_COLLECTION", "bge_small_finetuned_astra_collection")


settings = Settings()

SRC_DIR: str = os.path.dirname(__file__)
DATA_DIR: str = os.path.join(SRC_DIR, "../../data")
MODELS_DIR: str = os.path.join(SRC_DIR, "../../models")
CHROMA_DIR: str = os.path.join(SRC_DIR, "../../.chroma")
CHROMA_DB: str = os.path.join(CHROMA_DIR, settings.chroma_db)
CHROMA_COLLECTION: str =  settings.chroma_collection
HF_MODELS_REPO: str = "NenJa/astra-models"
HF_CHROMADB_REPO: str = "NenJa/astra-chromadb"
