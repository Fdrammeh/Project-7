"""
Module 7 Project — Semantic Search Engine
==========================================
evaluate.py — precision and recall for your search system

Run with:
    python evaluate.py
    python evaluate.py --n-results 5 --threshold 0.4

Define your evaluation set in EVAL_SET, then run this script against
different index configurations (different chunk sizes) to compare results.
"""

import argparse
from search import search


# Define your evaluation set here.
# Each entry needs a query and the source filenames you expect to be relevant.
# Use at least 5 queries for the chunking experiment.
EVAL_SET = [
    {
        "query": "How do I create a FastAPI API?",
        "relevant_sources": ["fastapi.txt", "rest-apis.txt"]
    },
    {
        "query": "What are embeddings and vectors?",
        "relevant_sources": ["embeddings-and-vectors.txt", "llms-and-ai.txt"]
    },
    {
        "query": "How do I build a Streamlit application?",
        "relevant_sources": ["streamlit.txt", "python-fundamentals.txt"]
    },
    {
        "query": "How do SQL databases work?",
        "relevant_sources": ["sql-databases.txt"]
    },
    {
        "query": "What are advanced Python programming concepts?",
        "relevant_sources": ["python-advanced.txt", "python-fundamentals.txt"]
    },
]


def precision_recall(
    retrieved_sources: list[str], relevant_sources: list[str]
) -> tuple[float, float]:
    """
    Compute source-level precision and recall.

    Returns (precision, recall) as floats in [0, 1].
    """
    retrieved = set(retrieved_sources)
    relevant = set(relevant_sources)

    if not retrieved:
        return 0.0, 0.0

    if not relevant:
        return 0.0, 0.0

    matches = retrieved & relevant

    precision = len(matches) / len(retrieved)
    recall = len(matches) / len(relevant)

    return precision, recall



def evaluate(n_results: int = 5, distance_threshold: float = None):
    """
    Run every query in EVAL_SET and print per-query and average precision/recall.
    """
    total_precision = 0.0
    total_recall = 0.0

    print("=== Search Evaluation ===")

    for item in EVAL_SET:
        query = item["query"]
        relevant_sources = item["relevant_sources"]

        results = search(
            query=query,
            n_results=n_results,
            distance_threshold=distance_threshold
        )

        retrieved_sources = [
            result["source"]
            for result in results
        ]

        precision, recall = precision_recall(
            retrieved_sources,
            relevant_sources
        )

        total_precision += precision
        total_recall += recall

        print(f"\nQuery: {query}")
        print(f"Expected: {relevant_sources}")
        print(f"Retrieved: {retrieved_sources}")
        print(f"Precision: {precision:.2f}")
        print(f"Recall: {recall:.2f}")

    count = len(EVAL_SET)

    if count > 0:
        average_precision = total_precision / count
        average_recall = total_recall / count

        print("\n=== Average ===")
        print(f"Precision: {average_precision:.2f}")
        print(f"Recall: {average_recall:.2f}")        


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate search quality")
    parser.add_argument("--n-results", type=int,   default=5)
    parser.add_argument("--threshold", type=float, default=None)
    args = parser.parse_args()
    evaluate(n_results=args.n_results, distance_threshold=args.threshold)
