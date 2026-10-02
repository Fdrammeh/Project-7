"""
Module 7 Project — Semantic Search Engine
==========================================
app.py — Streamlit search interface

Run with:
    streamlit run app.py

Make sure you've indexed documents first:
    python ingest.py
"""

import streamlit as st
from search import search, get_collection_stats
from ingest import (
    ingest,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_OVERLAP

)


# Page configuration
st.set_page_config(
    page_title="Semantic Search Engine",
    page_icon="🔎",
    layout="wide"
)


# Title
st.title("🔎 Semantic Search Engine")

st.write(
    "Search your document collection using natural language."
)


# Sidebar
st.sidebar.header("Search Settings")


# Number of results
n_results = st.sidebar.slider(
    "Number of results",
    min_value=1,
    max_value=10,
    value=5
)


# Distance threshold
distance_threshold = st.sidebar.slider(
    "Distance threshold",
    min_value=0.0,
    max_value=2.0,
    value=2.0,
    step=0.05
)


# Collection statistics
stats = get_collection_stats()

st.sidebar.metric(
    "Indexed chunks",
    stats["total_chunks"]
)

st.sidebar.metric(
    "Documents",
    stats["unique_sources"]
)

st.sidebar.subheader("Re-index Documents")

chunk_size = st.sidebar.number_input(
    "Chunk size",
    min_value=100,
    max_value=2000,
    value=DEFAULT_CHUNK_SIZE,
    step=50
)

overlap = st.sidebar.number_input(
    "Chunk overlap",
    min_value=0,
    max_value=chunk_size - 1,
    value=min(DEFAULT_OVERLAP, chunk_size - 1),
    step=10
)

if st.sidebar.button("🔄 Re-index Documents"):
    with st.spinner("Re-indexing documents..."):
        ingest(
            chunk_size=int(chunk_size),
            overlap=int(overlap)
        )

    st.success("Documents re-indexed successfully!")

    st.rerun()


# Source filter
source_options = stats["source_names"]

selected_sources = st.sidebar.multiselect(
    "Filter by source",
    options=source_options
)


# Search box
query = st.text_input(
    "Enter your search question:",
    placeholder="Example: How do I create a FastAPI endpoint?"
)


# Search
if query:
    results = search(
        query=query,
        n_results=n_results,
        sources=selected_sources if selected_sources else None,
        distance_threshold=distance_threshold
    )

    if not results:
        st.warning("No matching results found.")

    else:
        st.subheader("Search Results")

        for i, result in enumerate(results, start=1):
            st.markdown(
                f"### {i}. {result['source']}"
            )

            st.write(result["text"])

            st.caption(
                f"Chunk: {result['chunk_index']} | "
                f"Distance: {result['distance']:.4f} | "
                f"Score: {result['score']:.4f}"
            )

            st.divider()