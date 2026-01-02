from typing import Literal, List, Union
import numpy as np
import os

from sentence_transformers import SentenceTransformer
from src.settings import MODELS_DIR

# experiment with "BAAI/bge-large-en-v1.5" & "BAAI/bge-base-en-v1.5" later
EMBED_MODEL = Literal["BAAI/bge-small-en-v1.5", "BAAI/bge-base-en-v1.5", "BAAI/bge-large-en-v1.5"]


def sentence_embed(
  texts: str | List[str], model_name_or_path: Union[str, EMBED_MODEL] = "BAAI/bge-large-en-v1.5", device: str = "cpu"
) -> list[list[float]]:
  """
    Embeds the given texts using the specified model.

    Args:
        texts (str | List[str]): The list of texts or text to embed.
        model_name_or_path (Union[str, EMBED_MODEL]): The embedding model to use.
            Can be:
            - A HuggingFace Hub identifier (e.g., "BAAI/bge-large-en-v1.5" or "username/repo-name")
            - A local path relative to MODELS_DIR (e.g., "bge-small_finetuned")
            - An absolute path
        device (str): Device to use for encoding (default: "cpu").

    Returns:
        list[list[float]]: The embeddings of the texts.
    """
  # Check if it's a local path (starts with / or ./ or exists in MODELS_DIR)
  local_model_path = os.path.join(MODELS_DIR, model_name_or_path)
  
  # If it's a HuggingFace Hub identifier (contains /) or local path exists, use it directly
  # SentenceTransformer handles both HF Hub identifiers and local paths
  if os.path.exists(local_model_path):
    model_path = local_model_path
  else:
    # Assume it's either an HF Hub identifier or a local path that doesn't exist yet
    # SentenceTransformer will handle HF Hub downloads automatically
    model_path = model_name_or_path
  
  model = SentenceTransformer(model_path)
  embeddings: np.ndarray = model.encode(sentences=texts, device=device, show_progress_bar=True)
  embeddings_list: list = embeddings.tolist()
  return embeddings_list