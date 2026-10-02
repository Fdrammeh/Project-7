"""
Module 7 Project — Semantic Search Engine
==========================================
search.py — query ChromaDB and return ranked results

Import this module into app.py:
    from search import search, get_collection_stats
"""

from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# ── Configuration (must match ingest.py) ─────────────────────────────────────
CHROMA_PATH     = Path("chroma_data")
COLLECTION_NAME = "semantic_search"
MODEL_NAME      = "all-MiniLM-L6-v2"


def get_collection():
    """Return the persistent ChromaDB collection."""
    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    return collection


def search(
    query: str,
    n_results: int = 5,
    sources: list[str] = None,
    distance_threshold: float = None,
) -> list[dict]:
    """
    Search the ChromaDB collection and return ranked results.

    Args:
        query:              Natural language search query.
        n_results:          Maximum number of results to return.
        sources:            If provided, only return chunks from these filenames.
        distance_threshold: If provided, exclude results with distance above this
                            value (lower = more similar).

    Returns:
        List of result dicts sorted by distance ascending (best first):
            {
                "text":        str,
                "source":      str,
                "chunk_index": int,
                "distance":    float,
                "score":       float,  # 1 - distance
            }
        Returns [] for empty queries or if the collection has no documents.
    """
    # 1. Handle an empty search
    if not query or not query.strip():
        return []

    # 2. Get the ChromaDB collection
    collection = get_collection()

    # 3. Check whether the collection contains documents
    if collection.count() == 0:
        return []

    # 4. Load the same embedding model used during ingestion
    model = SentenceTransformer(MODEL_NAME)

    # 5. Convert the user's query into an embedding
    query_embedding = model.encode([query]).tolist()

    # 6. Build optional filters
    where = None

    if sources:
        where = {
            "source": {
                "$in": sources
            }
        }

    # 7. Search ChromaDB
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
        where=where
    )

    # 8. Prepare the results
    formatted_results = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for text, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        # 9. Apply the distance threshold if one was provided
        if distance_threshold is not None:
            if distance > distance_threshold:
                continue

        formatted_results.append({
            "text": text,
            "source": metadata["source"],
            "chunk_index": metadata["chunk_index"],
            "distance": float(distance),
            "score": 1 - float(distance)
        })

    # 10. Make sure the best results come first
    formatted_results.sort(
        key=lambda result: result["distance"]
    )

    return formatted_results


def get_collection_stats() -> dict:
    """
    Return basic stats about the indexed collection.

    Returns:
        {
            "total_chunks":   int,
            "unique_sources": int,
            "source_names":   list[str],
        }
    """
    # Get the ChromaDB collection
    collection = get_collection()

    # Find out how many chunks are stored
    total_chunks = collection.count()

    # If there are no chunks, return empty stats
    if total_chunks == 0:
        return {
            "total_chunks": 0,
            "unique_sources": 0,
            "source_names": []
        }

    # Get the metadata for all stored chunks
    results = collection.get(
        include=["metadatas"]
    )

    # Get the source filename from each chunk
    source_names = set()

    for metadata in results["metadatas"]:
        if metadata and "source" in metadata:
            source_names.add(metadata["source"])

    # Convert the set to a sorted list
    source_names = sorted(source_names)

    return {
        "total_chunks": total_chunks,
        "unique_sources": len(source_names),
        "source_names": source_names
    }

if __name__ == "__main__":
    results = search("How do I create an API?")

    print("\n=== Search Results ===")

    for i, result in enumerate(results, start=1):
        print(f"\n{i}. {result['source']}")
        print(f"   Chunk: {result['chunk_index']}")
        print(f"   Distance: {result['distance']:.4f}")
        print(f"   Score: {result['score']:.4f}")
        print(f"   Text: {result['text'][:200]}...")