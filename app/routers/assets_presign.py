
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
import os, uuid, datetime
from ..auth import get_current_user, require_owner_or_admin
from ..utils.s3 import generate_presigned_put, upload_file as s3_upload
from dotenv import load_dotenv
load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET") or None

router = APIRouter()

@router.post("/{project_id}/presign", response_model=schemas.PresignResponse)
def presign_upload(project_id: int, payload: schemas.PresignRequest, db: Session = Depends(get_db), user = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id==project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    # check ownership/admin
    require_owner_or_admin(user, project.owner_id)

    filename = payload.filename
    key = f"uploads/{project_id}/{uuid.uuid4().hex}_{filename}"
    if not S3_BUCKET:
        raise HTTPException(status_code=400, detail="S3_BUCKET not configured")
    url = generate_presigned_put(S3_BUCKET, key, expires_in=900)
    return {"url": url, "key": key, "method": "PUT"}

@router.post("/{project_id}/assets/register", response_model=schemas.AssetOut)
def register_asset(project_id: int, payload: schemas.RegisterAssetIn, db: Session = Depends(get_db), user = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id==project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    require_owner_or_admin(user, project.owner_id)

    # create asset record pointing to S3 key; path left blank or set to s3://
    s3_key = payload.s3_key
    filename = payload.filename
    path = f"s3://{os.getenv('S3_BUCKET')}/{s3_key}" if s3_key else ""
    asset = models.Asset(project_id=project_id, filename=filename, path=path, s3_key=s3_key)
    db.add(asset); db.commit(); db.refresh(asset)
    return asset
