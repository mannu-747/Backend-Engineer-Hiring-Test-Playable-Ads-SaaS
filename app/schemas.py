
from pydantic import BaseModel
from typing import Optional
import datetime

class UserCreate(BaseModel):
    email: str
    password: str
    # role will be ignored on public register; admin can set role directly in DB
    role: Optional[str] = "user"

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PresignRequest(BaseModel):
    filename: str

class PresignResponse(BaseModel):
    url: str
    key: str
    method: str = "PUT"

class RegisterAssetIn(BaseModel):
    filename: str
    s3_key: str

class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    created_at: datetime.datetime
    class Config:
        orm_mode = True

class AssetOut(BaseModel):
    id: int
    project_id: int
    filename: str
    path: str
    s3_key: Optional[str]
    uploaded_at: datetime.datetime
    class Config:
        orm_mode = True

class JobCreate(BaseModel):
    asset_id: Optional[int] = None

class JobOut(BaseModel):
    id: int
    celery_id: Optional[str]
    status: str
    output_path: Optional[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    class Config:
        orm_mode = True

class AnalyticsIn(BaseModel):
    projectId: int
    eventType: str
