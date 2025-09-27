
Expanded Loom Demo Script - Playable Ads SaaS Backend (~3 minutes)

Total time: 3:00

0:00 - 0:10 (10s) - Title slide / Intro
- On-screen: "Playable Ads SaaS Backend - FastAPI + Celery"
- Say: "Hi, I'm [Your Name]. I'll show the backend in 3 minutes."

0:10 - 0:40 (30s) - Architecture (show small diagram or bullet points)
- On-screen: show bullets: FastAPI (API + docs), PostgreSQL (metadata), Redis+Celery (jobs), S3 (assets/outputs), FFmpeg (rendering)
- Say: "Quickly — FastAPI handles HTTP and Swagger docs, Redis + Celery handle asynchronous rendering so HTTP requests remain fast. Assets and outputs are stored in S3 and rendered by FFmpeg in the worker."

0:40 - 1:20 (40s) - Auth: register & login (live demo via curl or Postman)
- On-screen: terminal showing `curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d '{"email":"me@example.com","password":"pass"}'`
- Show response with id and then `curl -X POST http://localhost:8000/auth/login -F "username=me@example.com" -F "password=pass"`
- Say: "Register creates a user; login returns a JWT token used for subsequent requests."

1:20 - 1:50 (30s) - Create project & presign upload
- On-screen: `curl -X POST http://localhost:8000/projects -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"title":"My Ad Project","description":"Test"}'`
- Then `curl -X POST http://localhost:8000/projects/1/presign -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"filename":"ad.mp4"}'`
- Show JSON response with `url` and `key`.
- Say: "We create a project and request a presigned URL to upload a large asset directly to S3."

1:50 - 2:10 (20s) - Upload to presigned URL (brief)
- On-screen: `curl -X PUT "<url>" --upload-file ./ad.mp4 -H "Content-Type: video/mp4"`
- Say: "Upload the file directly to S3 using the presigned URL. This keeps the API lightweight."

2:10 - 2:30 (20s) - Register asset & enqueue render
- On-screen: `curl -X POST http://localhost:8000/projects/1/assets/register -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"filename":"ad.mp4","s3_key":"uploads/1/abcd_ad.mp4"}'`
- Then `curl -X POST http://localhost:8000/jobs/1/render -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{}'`
- Say: "After uploading to S3, we register the asset in the DB and enqueue a Celery render job."

2:30 - 2:45 (15s) - Check job status & results
- On-screen: `curl http://localhost:8000/jobs/1 -H "Authorization: Bearer <token>"`
- Show status transition pending -> processing -> done and show `output_s3_key` or `output_path`
- Say: "The job completes asynchronously and the worker stores the rendered output (and S3 key) in the job record."

2:45 - 3:00 (15s) - Wrap up & next steps
- On-screen: repo link and notes
- Say: "Repo includes README, Alembic SQL, Docker compose, and a short demo script. Next steps: presigned downloads, RBAC expansion, or front-end integration. Thanks!"

Tips for recording:
- Use the Swagger UI at `/docs` to click through endpoints if preferred
- Show environment variables (briefly) to explain S3 toggle and DB URL
- Keep the terminal commands visible and copy/paste tokens to save time
