
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
import os, shutil, uuid
from dotenv import load_dotenv
load_dotenv()
from ..utils.s3 import upload_file as s3_upload
S3_BUCKET = os.getenv("S3_BUCKET") or None

router = APIRouter()

@router.post("/{project_id}/assets", response_model=schemas.AssetOut)
def upload_asset(project_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id==project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    uploads_dir = os.path.join("uploads", str(project_id))
    os.makedirs(uploads_dir, exist_ok=True)
    filename = file.filename
    unique = f"{uuid.uuid4().hex}_{filename}"
    dest = os.path.join(uploads_dir, unique)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)

    s3_key = None
    if S3_BUCKET:
        try:
            s3_key = s3_upload(dest, S3_BUCKET, unique)
        except Exception as e:
            print("S3 upload failed:", e)

    asset = models.Asset(project_id=project_id, filename=filename, path=dest, s3_key=s3_key)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset
