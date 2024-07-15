from typing import Literal, List
import numpy as np
import os

from sentence_transformers import SentenceTransformer
from src.settings import MODELS_DIR

# experiment with "BAAI/bge-large-en-v1.5" & "BAAI/bge-base-en-v1.5" later
EMBED_MODEL = Literal["BAAI/bge-small-en-v1.5", "BAAI/bge-base-en-v1.5", "BAAI/bge-large-en-v1.5"]


def sentence_embed(
  texts: str | List[str], model_name_or_path: EMBED_MODEL = "BAAI/bge-large-en-v1.5", device: str = "cpu"
) -> list[list[float]]:
  """
    Embeds the given texts using the specified model.

    Args:
        texts (str | List[str], str]): The list of texts or text to embed.
        model (EMBED_MODEL): The embedding model to use.

    Returns:
        np.ndarray: The embeddings of the texts.
    """
  model = SentenceTransformer(os.path.join(MODELS_DIR, model_name_or_path))
  embeddings: np.ndarray = model.encode(sentences=texts, device=device, show_progress_bar=True)
  embeddings_list: list = embeddings.tolist()
  return embeddings_list