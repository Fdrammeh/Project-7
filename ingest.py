"""
Module 7 Project — Semantic Search Engine
==========================================
ingest.py — document loading, chunking, and ChromaDB storage

Run with:
    python ingest.py
    python ingest.py --chunk-size 200 --overlap 50
"""

import argparse
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

# ── Configuration ─────────────────────────────────────────────────────────────
DOCS_DIR        = Path("docs")
CHROMA_PATH     = Path("chroma_data")
COLLECTION_NAME = "semantic_search"
MODEL_NAME      = "all-MiniLM-L6-v2"
DEFAULT_CHUNK_SIZE = 500
DEFAULT_OVERLAP    = 100


def chunk_text(text, chunk_size=500, overlap=100) -> list[str]:
    """
    Split text into fixed-size chunks with overlap.

    Args:
        text:       Full document text.
        chunk_size: Maximum characters per chunk.
        overlap:    Characters of overlap between consecutive chunks.

    Returns:
        List of non-empty chunk strings.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap cannot be negative")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size]

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def load_documents(docs_dir: Path) -> list[dict]:
    """
    Read all .txt and .md files from docs_dir.

    Returns:
        List of dicts: {"filename": str, "text": str}
    """
    documents = []

    for file_path in docs_dir.iterdir():

        if file_path.suffix.lower() in [".txt", ".md"]:

            text = file_path.read_text(
                encoding="utf-8"
            )

            documents.append({
                "filename": file_path.name,
                "text": text
            })

    return documents


def ingest(chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_OVERLAP):
    """
    Full ingestion pipeline: load → chunk → embed → upsert.

    Each chunk is stored with metadata: source filename, chunk index,
    and the chunk size used — so experiments with different sizes can
    be compared without ambiguity.
    """
    # 1. Load the documents from the docs folder
    documents = load_documents(DOCS_DIR)

    # 2. Get the persistent ChromaDB collection
   

    # 2. Create a fresh ChromaDB collection
    client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass  # Collection may not exist yet

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
)

    # 3. Load the embedding model
    model = SentenceTransformer(MODEL_NAME)

    # Lists to hold everything we will store
    ids = []
    texts = []
    metadatas = []

    # 4. Go through every document
    for document in documents:
        filename = document["filename"]
        text = document["text"]

        # 5. Break the document into chunks
        chunks = chunk_text(
            text,
            chunk_size=chunk_size,
            overlap=overlap
        )

        # 6. Prepare each chunk for ChromaDB
        for chunk_index, chunk in enumerate(chunks):
            ids.append(f"{filename}-{chunk_index}")
            texts.append(chunk)

            metadatas.append({
                "source": filename,
                "chunk_index": chunk_index,
                "chunk_size": chunk_size
            })

    # 7. Create embeddings for all chunks
    embeddings = model.encode(texts).tolist()

    # 8. Store the chunks, embeddings, and metadata in ChromaDB
    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"Ingested {len(documents)} documents")
    print(f"Stored {len(texts)} chunks")
    print(f"Chunk size: {chunk_size}")
    print(f"Overlap: {overlap}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Index docs/ into ChromaDB")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    parser.add_argument("--overlap",    type=int, default=DEFAULT_OVERLAP)
    args = parser.parse_args()
    ingest(chunk_size=args.chunk_size, overlap=args.overlap)
