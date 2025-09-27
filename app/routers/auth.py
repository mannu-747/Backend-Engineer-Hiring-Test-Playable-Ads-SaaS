
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas
from ..auth import register_user, authenticate_user, create_token
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/register")
def register(payload: schemas.UserCreate):
    # public registration only allows role 'user'
    user = register_user(payload.email, payload.password, role="user")
    return {"id": user.id, "email": user.email}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_token({"sub": user.id, "email": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
