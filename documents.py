import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.database.database import get_db
from app.models.document import Document
from app.models.document_version import DocumentVersion
from app.schemas.document import DocumentUpdateRequest
from app.services.document_service import extract_text, create_docx
from app.services.rag_service import chunk_text, create_embedding


router = APIRouter(
    prefix="/api/documents",
    tags=["Documents"]
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".docx",
    ".md"
}


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    os.makedirs(
        settings.upload_dir,
        exist_ok=True
    )

    safe_name = (
        f"{uuid.uuid4()}"
        f"{extension}"
    )

    file_path = os.path.join(
        settings.upload_dir,
        safe_name
    )

    content = await file.read()

    with open(
        file_path,
        "wb"
    ) as output:

        output.write(content)

    try:
        extracted_text = extract_text(
            file_path
        )

    except Exception as error:

        os.remove(file_path)

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    document = Document(
        filename=file.filename,
        file_type=extension,
        file_path=file_path
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    chunks = chunk_text(
        extracted_text
    )

    for index, chunk in enumerate(chunks):

        embedding = create_embedding(
            chunk
        )

        # Store embeddings as JSON text
        # in the document version content.
        version = DocumentVersion(
            document_id=document.id,
            version_number=index + 1,
            content=chunk
        )

        db.add(version)

    db.commit()

    return {
        "message": "Document uploaded successfully",
        "document_id": document.id,
        "filename": file.filename,
        "chunks": len(chunks)
    }


@router.get("")
def list_documents(
    db: Session = Depends(get_db)
):

    documents = db.query(
        Document
    ).all()

    return documents


@router.get("/{document_id}")
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = db.query(
        Document
    ).filter(
        Document.id == document_id
    ).first()

    if not document:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document


@router.put("/{document_id}")
def update_document(
    document_id: int,
    request: DocumentUpdateRequest,
    db: Session = Depends(get_db)
):

    document = db.query(
        Document
    ).filter(
        Document.id == document_id
    ).first()

    if not document:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    latest = db.query(
        DocumentVersion
    ).filter(
        DocumentVersion.document_id ==
        document_id
    ).order_by(
        DocumentVersion.version_number.desc()
    ).first()

    next_version = 1

    if latest:
        next_version = (
            latest.version_number + 1
        )

    version = DocumentVersion(
        document_id=document_id,
        version_number=next_version,
        content=request.content
    )

    db.add(version)

    db.commit()

    return {
        "message": "Document updated",
        "document_id": document_id,
        "version": next_version
    }


@router.post("/create")
def create_document(
    title: str,
    content: str
):

    filename = (
        title.replace(" ", "_")
        + ".docx"
    )

    file_path = create_docx(
        content,
        filename
    )

    return {
        "message": "Document created",
        "filename": filename,
        "path": file_path
    }