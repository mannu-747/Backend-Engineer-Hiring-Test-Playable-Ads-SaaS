
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user

router = APIRouter()

@router.post("/")
def record_analytics(payload: schemas.AnalyticsIn, db: Session = Depends(get_db), user = Depends(get_current_user)):
    project = db.query(models.Project).filter(models.Project.id==payload.projectId).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    ev = models.Analytics(project_id=payload.projectId, event_type=payload.eventType)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return {"ok": True, "id": ev.id}
