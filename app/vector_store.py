import json
from pathlib import Path

import faiss
import numpy as np
from rank_bm25 import BM25Okapi

from app.pdf_processor import extract_text_from_pdf
from app.chunker import chunk_text
from app.embeddings import create_embeddings


VECTOR_STORE_DIR = Path("data/vector_store")

INDEX_FILE = VECTOR_STORE_DIR / "index.faiss"
METADATA_FILE = VECTOR_STORE_DIR / "metadata.json"
BM25_FILE = VECTOR_STORE_DIR / "bm25.json"


def build_vector_store(pdf_path: str):
    """
    Build a hybrid vector store using ONLY the selected PDF.

    Creates:
    - FAISS index for semantic search
    - BM25 data for keyword search
    - Metadata for source and page citations
    """

    pdf_path = Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    # --------------------------------
    # Extract PDF text
    # --------------------------------

    pages = extract_text_from_pdf(
        str(pdf_path)
    )

    all_chunks = []

    for page in pages:

        chunks = chunk_text(
            page["text"]
        )

        for chunk in chunks:

            all_chunks.append({
                "text": chunk,
                "source": pdf_path.name,
                "page": page["page"]
            })

    if not all_chunks:
        raise ValueError(
            "No text chunks were created from the PDF"
        )

    texts = [
        item["text"]
        for item in all_chunks
    ]

    print(
        f"Processing {pdf_path.name}..."
    )

    print(
        f"Creating embeddings for {len(texts)} chunks..."
    )

    # --------------------------------
    # Create embeddings
    # --------------------------------

    embeddings = create_embeddings(
        texts
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    # --------------------------------
    # Create FAISS index
    # --------------------------------

    # Inner product works as cosine similarity
    # because our embeddings are normalized.

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    # --------------------------------
    # Create BM25 data
    # --------------------------------

    tokenized_texts = [
        text.lower().split()
        for text in texts
    ]

    # Create BM25 object to validate
    # that the tokenized data is usable.

    BM25Okapi(
        tokenized_texts
    )

    # --------------------------------
    # Create vector store directory
    # --------------------------------

    VECTOR_STORE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------
    # Save FAISS index
    # --------------------------------

    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    # --------------------------------
    # Save metadata
    # --------------------------------

    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            all_chunks,
            f,
            indent=2,
            ensure_ascii=False
        )

    # --------------------------------
    # Save BM25 tokenized documents
    # --------------------------------

    with open(
        BM25_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            tokenized_texts,
            f,
            indent=2,
            ensure_ascii=False
        )

    # --------------------------------
    # Finished
    # --------------------------------

    print(
        "Vector store created successfully."
    )

    print(
        f"Active document: {pdf_path.name}"
    )

    print(
        f"Total chunks: {len(all_chunks)}"
    )

    print(
        f"Embedding dimension: {dimension}"
    )

    print(
        f"FAISS index: {INDEX_FILE}"
    )

    print(
        f"BM25 data: {BM25_FILE}"
    )


def search(query: str, top_k: int = 10):
    """
    Hybrid search using:

    1. FAISS semantic search
    2. BM25 keyword search

    Both search the chunks belonging to the
    currently active PDF.
    """

    # --------------------------------
    # Check vector store
    # --------------------------------

    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            "FAISS index not found. Upload a PDF first."
        )

    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            "Metadata not found. Upload a PDF first."
        )

    if not BM25_FILE.exists():
        raise FileNotFoundError(
            "BM25 index not found. Upload the PDF again."
        )

    # --------------------------------
    # Load FAISS
    # --------------------------------

    index = faiss.read_index(
        str(INDEX_FILE)
    )

    # --------------------------------
    # Load metadata
    # --------------------------------

    with open(
        METADATA_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        metadata = json.load(f)

    # --------------------------------
    # Load BM25 data
    # --------------------------------

    with open(
        BM25_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        tokenized_texts = json.load(f)

    if not metadata:
        return []

    # --------------------------------
    # Limit top_k
    # --------------------------------

    top_k = min(
        top_k,
        len(metadata)
    )

    # --------------------------------
    # FAISS semantic search
    # --------------------------------

    query_embedding = create_embeddings(
        [query]
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    faiss_scores, faiss_indices = index.search(
        query_embedding,
        top_k
    )

    # --------------------------------
    # BM25 keyword search
    # --------------------------------

    bm25 = BM25Okapi(
        tokenized_texts
    )

    query_tokens = query.lower().split()

    bm25_scores = bm25.get_scores(
        query_tokens
    )

    bm25_indices = np.argsort(
        bm25_scores
    )[::-1][:top_k]

    # --------------------------------
    # Combine candidates
    # --------------------------------

    candidate_indices = set(
        faiss_indices[0].tolist()
    )

    candidate_indices.update(
        bm25_indices.tolist()
    )

    # Remove invalid FAISS index
    candidate_indices.discard(-1)

    results = []

    # --------------------------------
    # Build candidate results
    # --------------------------------

    for index_position in candidate_indices:

        result = metadata[
            index_position
        ].copy()

        # Default FAISS score
        result["faiss_score"] = 0.0

        # Find FAISS score
        for position, idx in enumerate(
            faiss_indices[0]
        ):

            if idx == index_position:

                result["faiss_score"] = float(
                    faiss_scores[0][position]
                )

                break

        # BM25 score
        result["bm25_score"] = float(
            bm25_scores[index_position]
        )

        results.append(
            result
        )

    # --------------------------------
    # Normalize scores
    # --------------------------------

    max_faiss = max(
        [
            result["faiss_score"]
            for result in results
        ],
        default=1.0
    )

    max_bm25 = max(
        [
            result["bm25_score"]
            for result in results
        ],
        default=1.0
    )

    for result in results:

        # FAISS normalization
        if max_faiss != 0:

            faiss_normalized = (
                result["faiss_score"]
                / max_faiss
            )

        else:

            faiss_normalized = 0.0

        # BM25 normalization
        if max_bm25 != 0:

            bm25_normalized = (
                result["bm25_score"]
                / max_bm25
            )

        else:

            bm25_normalized = 0.0

        # --------------------------------
        # Hybrid score
        # --------------------------------

        result["combined_score"] = (
            0.6 * faiss_normalized
            +
            0.4 * bm25_normalized
        )

    # --------------------------------
    # Sort by hybrid score
    # --------------------------------

    results.sort(
        key=lambda result:
            result["combined_score"],
        reverse=True
    )

    # --------------------------------
    # Return best candidates
    # --------------------------------

    return results[:top_k]