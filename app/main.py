
from fastapi import FastAPI, Depends
from .database import engine, Base, get_db
import os
from dotenv import load_dotenv
load_dotenv()

# import routers
from .routers import projects, assets, jobs, analytics, auth, assets_presign
from . import models

# create directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# create tables (for quick dev). For production, use Alembic migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Playable Ads SaaS (FastAPI) - Updated")

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(assets.router, prefix="/projects", tags=["assets"])
app.include_router(assets_presign.router, prefix="/projects", tags=["presign_uploads"])

app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
