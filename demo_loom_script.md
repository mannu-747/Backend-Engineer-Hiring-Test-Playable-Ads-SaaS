
Loom Demo Script - Playable Ads SaaS Backend (<= 3 minutes)

1) Quick intro (15s)
- "Hi, I'm [Your Name]. This is a lightweight backend for a playable-ads SaaS built with FastAPI, Celery, and PostgreSQL/S3 compatible storage."

2) Architecture overview (30s)
- FastAPI handles HTTP API and Swagger docs.
- PostgreSQL (or SQLite for quick dev) stores metadata; Alembic scaffold included for migrations.
- Redis + Celery handle asynchronous render jobs so renders don't block requests.
- S3 stores uploaded assets and rendered outputs (optional; controlled by env vars).
- FFmpeg is used by the worker to overlay text on videos (or convert images to short videos).

3) Core flows (90s)
- Register and login: `/auth/register` and `/auth/login` (obtain JWT).
- Create project: `POST /projects` (JWT-protected).
- Upload asset: `POST /projects/{id}/assets` (multipart, optionally stored in S3).
- Start render: `POST /jobs/{project_id}/render` (enqueue Celery job).
- Check job: `GET /jobs/{job_id}` to inspect status and outputs.
- Analytics: `POST /analytics` to record events like impressions or clicks.

4) Notes & wrap-up (45s)
- To use Postgres, update `.env` DATABASE_URL and run Alembic or the provided SQL.
- To enable S3, set S3_BUCKET and credentials in `.env`.
- The repository includes sample assets and a README with setup steps.
- Ask me to demonstrate specific flows or extend permissions and presigned uploads.
