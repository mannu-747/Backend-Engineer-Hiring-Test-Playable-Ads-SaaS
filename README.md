
# Playable Ads SaaS - Backend (Python / FastAPI / Celery) - Updated

This project implements a backend prototype for a playable-ads SaaS.

## Highlights in this updated version
- JWT-based user registration & login
- Option for PostgreSQL with Alembic scaffold
- Celery + Redis job queue for video rendering jobs
- S3-compatible uploads/outputs via boto3 (optional)
- FFmpeg rendering with text overlay (images converted to short videos)
- Docker & docker-compose for Redis + API + Worker

## Quick start (dev)
1. Create virtualenv and install deps:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure .env (see `.env.example`):

3. Run Redis (local or docker compose):
```
docker-compose up -d redis
```

4. Start worker:
```
celery -A app.workers.celery_worker.celery_app worker --loglevel=info
```

5. Start API:
```
uvicorn app.main:app --reload --port 8000
```

6. API docs: http://localhost:8000/docs

## Notes
- By default the project uses SQLite for convenience. To use Postgres, set `DATABASE_URL` in `.env` to `postgresql+psycopg2://user:pass@host:port/dbname` and run Alembic migrations.
- S3 usage is optional. If you set `S3_BUCKET` and credentials in `.env`, uploaded assets and rendered outputs will be stored in S3.

## Presigned S3 uploads & Permissions

The API now supports presigned S3 PUT URLs to upload large assets directly to S3 without passing file bytes through the API server. Use `POST /projects/{project_id}/presign` with `{filename}` to receive a presigned PUT URL and `key`.

After uploading the file to the presigned URL, call `POST /projects/{project_id}/assets/register` with `{filename, s3_key}` to register the asset in the database.

Only the project owner or an `admin` role can create presigned URLs, register assets, or enqueue renders for a project. Public registration still creates role `user` by default.
