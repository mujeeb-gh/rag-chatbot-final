from typing import Any
import chromadb
from chromadb import Collection, QueryResult
from chromadb.api import ClientAPI
from pandas import DataFrame
from src.sentence import sentence_embed
from src.settings import CHROMA_COLLECTION, CHROMA_DIR

chroma_client: ClientAPI = chromadb.PersistentClient(path=CHROMA_DIR)
chroma_collection: Collection = chroma_client.get_or_create_collection(
    name=CHROMA_COLLECTION, metadata={"hnsw:space": "cosine"}
)


def ingest(
    data: DataFrame,
    doc_col: str,
    id_col: str | None,
    meta_col: list[str] | None = None,
) -> None:
    # Create a list of list of floats with the em
    _docs: list[str] = data[doc_col].tolist()

    # Create a list of str with the id column
    if id_col:
        _ids: list[str] = data[id_col].tolist()
    else:
        _ids = [str(i) for i in range(len(data))]

    # Create a list of dictionaries with the metadata columns
    if meta_col:
        _metas: list[dict[str, Any]] | None = data[meta_col].to_dict(orient="records")  # type: ignore
    else:
        _metas = None

    # Embed the documents
    _embeds: list[list[float]] = sentence_embed(texts=_docs)  # type: ignore

    # Ingest the documents
    chroma_collection.add(  # type: ignore
        documents=_docs,
        embeddings=_embeds,  # type: ignore
        metadatas=_metas,  # type: ignore
        ids=_ids,
    )


def search(
    query: str,
    k: int = 5,
) -> list[dict[str, Any]] | None:
    # Embed the query
    _embed: list[list[float]] = sentence_embed(texts=query, model_name_or_path="models/bge-large_finetuned")  # type: ignore

    # Search the collection
    _results: QueryResult = chroma_collection.query(  # type: ignore
        query_embeddings=_embed,
        n_results=k,
        include=["documents", "distances", "metadatas"],
    )

    # Return if there is no result
    if not _results["documents"]:
        return None

    docs: list[str] = _results["documents"][0] if _results["documents"] else []
    scores: list[float] = _results["distances"][0] if _results["distances"] else []
    metadatas = _results["metadatas"][0] if _results["metadatas"] else []

    return [{"doc": doc, "score": score, "metadata": metadata} for doc, score, metadata in zip(docs, scores, metadatas)]


chroma_collection = 'bge_large_finetuned_astra_collection'
chroma_dir = "embeddings/bge-large-finetuned-chroma"

chroma_client: ClientAPI = chromadb.PersistentClient(path=chroma_dir)
chroma_collection: Collection = chroma_client.get_or_create_collection(
    name=chroma_collection, metadata={"hnsw:space": "cosine"}
)
def search_eval(
    query: str,
    k: int = 5,
    model_name_or_path = "BAAI/bge-small-en-v1.5"
) -> list[dict[str, Any]] | None:
    # Embed the query
    _embed: list[list[float]] = sentence_embed(query, model_name_or_path=model_name_or_path)  # type: ignore

    # Search the collection
    _results: QueryResult = chroma_collection.query(  # type: ignore
        query_embeddings=_embed,
        n_results=k,
        include=["documents", "distances", "metadatas"],
    )

    # Return if there is no result
    if not _results["documents"]:
        return None

    docs: list[str] = _results["documents"][0] if _results["documents"] else []
    scores: list[float] = _results["distances"][0] if _results["distances"] else []
    metadatas = _results["metadatas"][0] if _results["metadatas"] else []

    return [{"doc": doc, "score": score, "metadata": metadata} for doc, score, metadata in zip(docs, scores, metadatas)]