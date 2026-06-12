"""
RAG Service — Retrieval-Augmented Generation pipeline.

Handles PDF parsing, text chunking, embedding generation,
and similarity search using ChromaDB as the vector store
and Google's embedding model.
"""

import os
import uuid
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import chromadb

from core.config import settings


# ---------------------------------------------------------------------------
# ChromaDB client (persistent storage)
# ---------------------------------------------------------------------------

CHROMA_DB_DIR = Path(__file__).parent.parent / "chroma_data"
UPLOADS_DIR = Path(__file__).parent.parent / "uploads"
UPLOADS_DIR.mkdir(exist_ok=True)
CHROMA_DB_DIR.mkdir(exist_ok=True)

chroma_client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))


def _get_embeddings():
    """Get the Google embedding function for ChromaDB."""
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured")
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2",
        google_api_key=settings.GEMINI_API_KEY,
    )


def _get_user_collection(user_id: int):
    """Get or create a ChromaDB collection for the user."""
    return chroma_client.get_or_create_collection(
        name=f"user_{user_id}_docs",
        metadata={"hnsw:space": "cosine"},
    )


# ---------------------------------------------------------------------------
# PDF Processing Pipeline
# ---------------------------------------------------------------------------

def process_pdf(file_path: str, user_id: int) -> int:
    """
    Process a PDF file through the RAG pipeline:
    1. Load PDF → extract text per page
    2. Split text into chunks
    3. Generate embeddings and store in ChromaDB

    Returns the number of chunks created.
    """
    # 1. Load PDF
    loader = PyPDFLoader(file_path)
    pages = loader.load()

    if not pages:
        return 0

    # 2. Split into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = text_splitter.split_documents(pages)

    if not chunks:
        return 0

    # 3. Generate embeddings and store in ChromaDB
    embeddings_model = _get_embeddings()
    collection = _get_user_collection(user_id)

    # Prepare data for ChromaDB
    texts = [chunk.page_content for chunk in chunks]
    metadatas = [
        {
            "source": os.path.basename(file_path),
            "page": chunk.metadata.get("page", 0),
        }
        for chunk in chunks
    ]
    ids = [str(uuid.uuid4()) for _ in chunks]

    # Generate embeddings in batches
    batch_size = 50
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i : i + batch_size]
        batch_metadatas = metadatas[i : i + batch_size]
        batch_ids = ids[i : i + batch_size]

        batch_embeddings = embeddings_model.embed_documents(batch_texts)

        collection.add(
            documents=batch_texts,
            embeddings=batch_embeddings,
            metadatas=batch_metadatas,
            ids=batch_ids,
        )

    return len(chunks)


# ---------------------------------------------------------------------------
# Similarity Search
# ---------------------------------------------------------------------------

def search_documents(query: str, user_id: int, n_results: int = 5) -> list[str]:
    """
    Search the user's document collection for chunks relevant to the query.

    Returns a list of text chunks ranked by similarity.
    """
    collection = _get_user_collection(user_id)

    # Check if collection has any documents
    if collection.count() == 0:
        return []

    embeddings_model = _get_embeddings()
    query_embedding = embeddings_model.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count()),
    )

    if results and results["documents"]:
        return results["documents"][0]  # First query's results

    return []


def get_user_document_count(user_id: int) -> int:
    """Return the number of chunks in the user's vector store."""
    collection = _get_user_collection(user_id)
    return collection.count()
