"""
Documents router — API endpoints for document upload and management.

Allows users to upload PDFs that get processed through the RAG pipeline,
enabling Aurora to answer questions based on document content.
"""

import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from core.dependencies import get_current_user, get_db
from models.user import User
from models.document import Document
from schemas.document import DocumentResponse
from services.rag_service import process_pdf, UPLOADS_DIR


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a PDF document and process it through the RAG pipeline.
    The document content will be chunked, embedded, and stored in the
    vector database for context-aware AI responses.
    """
    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )

    # Validate file size (max 10MB)
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size exceeds 10MB limit",
        )

    # Save file to disk
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = UPLOADS_DIR / unique_name

    with open(file_path, "wb") as f:
        f.write(contents)

    # Create database record
    db_document = Document(
        filename=unique_name,
        original_name=file.filename,
        file_size=len(contents),
        status="processing",
        user_id=current_user.id,
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    # Process through RAG pipeline
    try:
        chunk_count = process_pdf(str(file_path), current_user.id)
        db_document.chunk_count = chunk_count
        db_document.status = "ready"
        db.commit()
        db.refresh(db_document)
    except Exception as e:
        print(f"Error processing document: {e}")
        db_document.status = "failed"
        db.commit()
        db.refresh(db_document)
        # Clean up the file on failure
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}",
        )

    return db_document


@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return all documents uploaded by the authenticated user."""
    return (
        db.query(Document)
        .filter(Document.user_id == current_user.id)
        .order_by(Document.created_at.desc())
        .all()
    )


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a document and its associated vector data."""
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    if doc.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Delete the file from disk
    file_path = UPLOADS_DIR / doc.filename
    if file_path.exists():
        os.remove(file_path)

    # Delete from database
    db.delete(doc)
    db.commit()
