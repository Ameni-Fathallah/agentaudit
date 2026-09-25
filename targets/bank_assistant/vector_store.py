"""Embeddings et base vectorielle ChromaDB pour le RAG de BanqueNova.

Usage (construire l'index) : uv run python -m targets.bank_assistant.vector_store
"""

from collections import Counter
from contextlib import suppress

import chromadb
import numpy as np
from ollama import Client

from targets.bank_assistant.chunking import load_chunks
from targets.config import settings

COLLECTION_NAME = "banquenova_documents"

ollama_client = Client(host=settings.ollama_base_url)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Transforme des textes en vecteurs normalisés (de longueur 1)."""
    response = ollama_client.embed(model=settings.embedding_model, input=texts)
    vectors = np.array(response.embeddings, dtype=np.float32)
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors.tolist()


def get_chroma_client():
    return chromadb.PersistentClient(path=settings.vector_store_path)


def build_index() -> None:
    """Construit l'index vectoriel à partir de tous les documents.

    FAILLE VOLONTAIRE : les documents internes sont indexés avec les documents
    publics, sans aucun contrôle d'accès.
    """
    chunks = load_chunks()
    client = get_chroma_client()

    # On repart de zéro pour que l'index reflète exactement les documents actuels.
    with suppress(Exception):
        client.delete_collection(COLLECTION_NAME)
    collection = client.create_collection(COLLECTION_NAME, embedding_function=None)

    collection.add(
        ids=[chunk.chunk_id for chunk in chunks],
        documents=[chunk.text for chunk in chunks],
        metadatas=[
            {"source": chunk.source, "visibility": chunk.visibility, "section": chunk.section}
            for chunk in chunks
        ],
        embeddings=embed_texts([chunk.text for chunk in chunks]),
    )

    counts = Counter(chunk.visibility for chunk in chunks)
    print(f"Index construit : {len(chunks)} chunks ({dict(counts)})")


def search(question: str, top_k: int | None = None) -> list[dict]:
    """Renvoie les chunks les plus proches de la question, du plus proche au moins proche."""
    collection = get_chroma_client().get_collection(COLLECTION_NAME, embedding_function=None)
    results = collection.query(
        query_embeddings=embed_texts([question]),
        n_results=top_k or settings.rag_top_k,
    )
    return [
        {
            "text": document,
            "source": metadata["source"],
            "visibility": metadata["visibility"],
            "distance": distance,
        }
        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
            strict=True,
        )
    ]


if __name__ == "__main__":
    build_index()
