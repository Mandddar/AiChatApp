"""
RAG Service — Retrieval-Augmented Generation pipeline.

Handles PDF parsing, text chunking, embedding generation,
and similarity search using Pinecone as the vector store
and Google's embedding model.
"""

import os
import uuid
import tempfile
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore

from core.config import settings

# ---------------------------------------------------------------------------
# Setup and Configuration
# ---------------------------------------------------------------------------

UPLOADS_DIR = Path(tempfile.gettempdir()) / "aichatapp_uploads"
UPLOADS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Pinecone Client
# ---------------------------------------------------------------------------

def _get_pinecone_index():
    if not settings.PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY is not configured")
    pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    return pc.Index(settings.PINECONE_INDEX_NAME)


def _get_embeddings():
    """Get the Google embedding function."""
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured")
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2",
        google_api_key=settings.GEMINI_API_KEY,
    )

def _get_vectorstore():
    return PineconeVectorStore(
        index=_get_pinecone_index(),
        embedding=_get_embeddings(),
        text_key="text"
    )

# ---------------------------------------------------------------------------
# PDF Processing Pipeline
# ---------------------------------------------------------------------------

def process_pdf(file_path: str, user_id: int) -> int:
    """
    Process a PDF file through the RAG pipeline:
    1. Load PDF → extract text per page
    2. Split text into chunks
    3. Generate embeddings and store in Pinecone
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

    # 3. Add metadata to chunks
    filename = os.path.basename(file_path)
    for chunk in chunks:
        # Save source filename for deletion later
        chunk.metadata["source"] = filename
        chunk.metadata["user_id"] = user_id

    # 4. Generate embeddings and store in Pinecone
    vectorstore = _get_vectorstore()
    
    # Use Pinecone namespace to separate user data
    namespace = f"user_{user_id}"
    
    # Generate unique IDs for documents
    ids = [str(uuid.uuid4()) for _ in chunks]

    # Batching is handled by Langchain Pinecone internally, but we can just call add_documents
    vectorstore.add_documents(documents=chunks, ids=ids, namespace=namespace)

    return len(chunks)


# ---------------------------------------------------------------------------
# Similarity Search & Management
# ---------------------------------------------------------------------------

def search_documents(query: str, user_id: int, n_results: int = 5) -> list[str]:
    """
    Search the user's document collection for chunks relevant to the query.
    """
    vectorstore = _get_vectorstore()
    namespace = f"user_{user_id}"
    
    try:
        results = vectorstore.similarity_search(
            query, 
            k=n_results, 
            namespace=namespace
        )
        
        if results:
            return [doc.page_content for doc in results]
    except Exception as e:
        print(f"Error searching Pinecone: {e}")
        
    return []

def get_user_document_count(user_id: int) -> int:
    """Return the number of chunks in the user's vector store namespace."""
    namespace = f"user_{user_id}"
    try:
        index = _get_pinecone_index()
        stats = index.describe_index_stats()
        
        if "namespaces" in stats and namespace in stats["namespaces"]:
            return stats["namespaces"][namespace]["vector_count"]
    except Exception as e:
        print(f"Error getting stats from Pinecone: {e}")
        
    return 0

def delete_document_vectors(user_id: int, filename: str):
    """Delete all vectors associated with a specific file from Pinecone."""
    namespace = f"user_{user_id}"
    try:
        index = _get_pinecone_index()
        # Delete by metadata filter
        index.delete(
            filter={"source": {"$eq": filename}},
            namespace=namespace
        )
    except Exception as e:
        print(f"Error deleting vectors from Pinecone: {e}")
