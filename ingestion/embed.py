"""
ingestion/embed.py
==================

Reads Markdown files from `data/chunks/` and embeds them into a local
ChromaDB collection at `data/chroma/`. Each Markdown file is split into
overlapping ~500-token chunks; each chunk becomes a 384-dim vector plus
its original text plus minimal metadata.

Pipeline:
    data/chunks/<slug>.md  ->  data/chroma/  (persistent Chroma collection)

Embedding model: BAAI/bge-small-en-v1.5  (small, fast, top-tier quality
on English retrieval benchmarks, runs on CPU, no API key needed).

Why ~500 tokens per chunk:
- 500 tokens ≈ 350-400 English words ≈ 2-3 paragraphs
- Large enough to carry a coherent claim with context
- Small enough that retrieval stays focused (the LLM doesn't get drowned
  in irrelevant prose)

Why 50-token overlap:
- Without overlap, a sentence split across two chunks loses half its
  meaning in each
- With overlap, each chunk has some surrounding context
- Standard practice (LangChain, LlamaIndex defaults are similar)

Run:
    python ingestion/embed.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parent.parent
CHUNKS_DIR = ROOT / "data" / "chunks"
CHROMA_DIR = ROOT / "data" / "chroma"
COLLECTION_NAME = "myjoblens_corpus"
EMBED_MODEL_NAME = "BAAI/bge-small-en-v1.5"
CHUNK_SIZE_WORDS = 500
CHUNK_OVERLAP_WORDS = 50

def chunk_text(text: str, size: int, overlap: int) -> list[str]:
    """
    Sliding-window word chunker. Splits text on whitespace, yields
    consecutive `size`-word windows with `overlap` words of context
    shared between adjacent windows.
    """
    words = text.split()
    if not words:
        return []
    step = max(1, size - overlap)
    out: list[str] = []
    for start in range(0, len(words), step):
        piece = words[start:start + size]
        if not piece:
            break
        out.append(" ".join(piece))
        if start + size >= len(words):
            break
    return out

def embed_file(path: Path, model: SentenceTransformer,
               collection) -> int:
    """Read one .md, chunk + embed + upsert into the Chroma collection.
    Returns the number of chunks added.
    """
    text = path.read_text(encoding="utf-8", errors="ignore")
    chunks = chunk_text(text, CHUNK_SIZE_WORDS, CHUNK_OVERLAP_WORDS)
    if not chunks:
        return 0
    embeddings = model.encode(chunks, normalize_embeddings=True).tolist()
    ids = [f"{path.stem}::{i:04d}" for i in range(len(chunks))]
    metadatas = [{"source_file": path.name, "chunk_index": i}
                 for i in range(len(chunks))]
    collection.upsert(ids=ids, documents=chunks,
                      embeddings=embeddings, metadatas=metadatas)
    return len(chunks)

def main() -> int:
    if not CHUNKS_DIR.exists():
        print(f"Missing chunks dir: {CHUNKS_DIR}", file=sys.stderr)
        return 1
    md_files = sorted(CHUNKS_DIR.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {CHUNKS_DIR}", file=sys.stderr)
        return 1
    print(f"Loading embedding model: {EMBED_MODEL_NAME}")
    model = SentenceTransformer(EMBED_MODEL_NAME)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    total = 0
    for path in md_files:
        n = embed_file(path, model, collection)
        total += n
        print(f"{path.name}: +{n} chunks")
    print(f"Done. {total} total chunks in collection '{COLLECTION_NAME}'.")
    return 0

if __name__ == "__main__":
    sys.exit(main())