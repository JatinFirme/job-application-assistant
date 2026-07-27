import os
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import get_db
from app.models.resume import Resume

# Grouping all resume-related endpoints under one router, mounted at
# /resumes in main.py. Every route below is relative to that prefix.
router = APIRouter(prefix="/resumes", tags=["resumes"])

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # --- 1. Validate ---
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Only {', '.join(ALLOWED_EXTENSIONS)} files are allowed",
        )

    # --- 2. Save the file to disk ---
    os.makedirs(settings.upload_dir, exist_ok=True)

    # Never trust user-supplied filenames for storage -- generate a random
    # unique name instead. The ORIGINAL filename is kept in the DB column
    # below, purely for display purposes.
    stored_filename = f"{uuid.uuid4().hex}{ext}"
    storage_path = os.path.join(settings.upload_dir, stored_filename)

    contents = await file.read()
    with open(storage_path, "wb") as f:
        f.write(contents)

    # --- 3. Record it in the database ---
    resume = Resume(
        original_filename=file.filename,
        storage_path=storage_path,
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)  # pulls back the auto-generated id and uploaded_at

    return {
        "id": resume.id,
        "original_filename": resume.original_filename,
        "storage_path": resume.storage_path,
        "uploaded_at": resume.uploaded_at,
    }


@router.get("/")
def list_resumes(db: Session = Depends(get_db)):
    """
    Lists every uploaded resume. Mainly here so we have an easy way to
    verify uploads worked, without needing psql every time.
    """
    resumes = db.scalars(select(Resume)).all()
    return [
        {
            "id": r.id,
            "original_filename": r.original_filename,
            "storage_path": r.storage_path,
            "uploaded_at": r.uploaded_at,
        }
        for r in resumes
    ]
