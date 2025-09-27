
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from .database import SessionLocal
from . import models

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretreplace")
scheme = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_token(data: dict):
    # production should include expiry (exp)
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def register_user(email: str, password: str, role: str = "user"):
    db = SessionLocal()
    try:
        existing = db.query(models.User).filter(models.User.email==email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        user = models.User(email=email, hashed_password=get_password_hash(password), role=role)
        db.add(user); db.commit(); db.refresh(user)
        return user
    finally:
        db.close()

def authenticate_user(email: str, password: str):
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.email==email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    finally:
        db.close()

def get_current_user(creds: HTTPAuthorizationCredentials = Security(scheme)):
    token = creds.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        db = SessionLocal()
        user = db.query(models.User).filter(models.User.id==user_id).first()
        db.close()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_admin(user):
    if not user or getattr(user, "role", None) != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")

def require_owner_or_admin(user, project_owner_id):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    if user.role == "admin":
        return True
    if project_owner_id is None:
        raise HTTPException(status_code=403, detail="No owner assigned to project")
    if user.id != project_owner_id:
        raise HTTPException(status_code=403, detail="Not allowed. Only project owner or admin may perform this action.")
    return True
