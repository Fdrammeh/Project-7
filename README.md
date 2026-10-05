# Module 7 Project — Semantic Search Engine 

## Overview

Build a semantic search tool over a document collection. The tool loads, chunks,
embeds, and stores documents in ChromaDB, then provides a Streamlit interface
where users can type a question and see ranked results. You'll also run a
chunking experiment and document your findings.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Index the document corpus:
   ```bash
   python ingest.py
   ```

3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit search interface — your primary work file |
| `ingest.py` | Document loading, chunking, and ChromaDB storage |
| `search.py` | Search functions: query ChromaDB and rank results |
| `evaluate.py` | Evaluation framework: precision and recall |
| `docs/` | Starter document corpus (add your own documents here) |
| `chroma_data/` | Persistent ChromaDB storage (created on first run) |
| `requirements.txt` | Python dependencies |

## Requirements

See the project brief on the course platform for the full rubric. Key sections:

1. **Document Ingestion** — load `docs/` folder, configurable chunk size/overlap,
   store in ChromaDB with source and chunk-index metadata
2. **Semantic Search** — ranked results with scores, configurable `n_results` and
   threshold, edge-case handling
3. **Streamlit Interface** — search input, sidebar controls (filter, re-index,
   result count), at least one `st.metric()`
4. **Chunking Experiment** — re-index at 2+ chunk sizes, run 5 identical queries,
   compare and document findings in this README
5. **Code Quality** — docstrings, modular files, working `requirements.txt`

## Chunking Experiment Results

> Fill this section in after completing the experiment.

**Chunk sizes tested:** _e.g. 200 chars vs 500 chars_

**Test queries:**
1. How do I create a FastAPI API?
2. What are embeddings and vectors?
3. How do I build a Streamlit application?
4. How do SQL databases work?
5. What are advanced Python programming concepts?


**Findings:**

_Which chunk size performed better overall, and why?_
I tested 500-character chunks with 100-character overlap and 200-character chunks with 50-character overlap using the same five evaluation queries. With top-3 retrieval, both configurations achieved 1.00 precision and 0.60 recall. With top-5 retrieval, the 500-character configuration achieved 0.93 precision and 0.70 recall, while the 200-character configuration achieved 0.90 precision and 0.60 recall. For this document collection, the 500-character configuration produced stronger top-5 results, while both configurations performed identically on the top-3 average metrics.


Semantic Search Engine
Overview
This project is a semantic search tool that allows users to search a collection of documents using questions. The application uses Sentence Transformers to create embeddings and ChromaDB to store and search those embeddings.The application follows an ingest → search → Streamlit architecture. Documents are loaded, chunked, converted into embeddings with Sentence Transformers, and stored in ChromaDB.The Streamlit app searches the stored embeddings and displays ranked results with the source, distance, and relevance score. The project also includes search evaluation and a chunking experiment comparing 200-character and 500-character chunks.

Main files:

ingest.py — Loads documents, creates chunks, generates embeddings, and stores them in ChromaDB.

search.py — Performs semantic searches and returns ranked results.

app.py — Provides the Streamlit user interface.

evaluate.py — Tests search quality using precision and recall.

docs/ — Contains the documents used by the search engine.

chroma_data/ — Persistent ChromaDB storage.

requirements.txt — Lists the Python packages required to run the project.

Requirements
The project requires:
Python 3
ChromaDB
Sentence Transformers
Streamlit
A Python virtual environment is recommended.
Install the required packages with:
pip install -r requirements.txt
