import os

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv())


SRC_DIR: str = os.path.dirname(__file__)
DATA_DIR: str = os.path.join(SRC_DIR, "../../data")
CHROMA_DIR: str = os.path.join(SRC_DIR, "../../.chroma")
CHROMA_COLLECTION: str = "bge-large-finetuned-chroma"


class Settings(BaseSettings):
    cohere_api_key: str = ""
    groq_api_key: str = ""
    openai_api_key: str = ""


settings = Settings()
