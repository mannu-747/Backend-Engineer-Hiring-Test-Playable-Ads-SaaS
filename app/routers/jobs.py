
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..workers.tasks import render_video_task
from celery.result import AsyncResult
from ..auth import get_current_user, require_owner_or_admin

router = APIRouter()

@router.post("/{project_id}/render", response_model=schemas.JobOut)
def enqueue_render(project_id: int, payload: schemas.JobCreate = None, db: Session = Depends(get_db), user = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id==project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    require_owner_or_admin(user, project.owner_id)

    # find asset
    asset = None
    if payload and payload.asset_id:
        asset = db.query(models.Asset).filter(models.Asset.id==payload.asset_id, models.Asset.project_id==project_id).first()
    else:
        asset = db.query(models.Asset).filter(models.Asset.project_id==project_id).order_by(models.Asset.uploaded_at.desc()).first()
    if not asset:
        raise HTTPException(status_code=400, detail="No asset found for project. Upload an asset first.")

    job = models.Job(project_id=project_id, status=models.JobStatus.pending, input_asset_id=asset.id)
    db.add(job)
    db.commit()
    db.refresh(job)

    async_res = render_video_task.apply_async(args=[job.id, asset.path])
    job.celery_id = async_res.id
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.get("/{job_id}", response_model=schemas.JobOut)
def get_job(job_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    job = db.query(models.Job).filter(models.Job.id==job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    # load project owner
    project = db.query(models.Project).filter(models.Project.id==job.project_id).first()
    require_owner_or_admin(user, project.owner_id if project else None)
    if job.celery_id:
        try:
            result = AsyncResult(job.celery_id)
            state = result.state.lower()
            if state == "pending":
                job.status = models.JobStatus.pending
            elif state in ("started","inprogress","progress"):
                job.status = models.JobStatus.processing
            elif state == "success":
                job.status = models.JobStatus.done
            elif state == "failure":
                job.status = models.JobStatus.failed
        except Exception:
            pass
    db.add(job); db.commit(); db.refresh(job)
    return job
