
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.ProjectOut)
def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    project = models.Project(title=payload.title, description=payload.description, owner_id=user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
