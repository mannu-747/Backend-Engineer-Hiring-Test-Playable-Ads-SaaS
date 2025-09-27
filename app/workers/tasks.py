
from .celery_worker import celery_app
from .. import models
from ..database import SessionLocal
from ..utils.ffmpeg_utils import simulate_render
import time, os

@celery_app.task(bind=True)
def render_video_task(self, job_db_id: int, asset_path: str):
    db = SessionLocal()
    try:
        job = db.query(models.Job).filter(models.Job.id==job_db_id).first()
        if not job:
            return {"error": "job not found"}
        job.status = models.JobStatus.processing
        db.add(job); db.commit(); db.refresh(job)

        # simulate processing time
        time.sleep(2)

        outputs_dir = os.path.join("outputs", str(job.project_id))
        result = simulate_render(asset_path, outputs_dir, text_overlay="PlayableAd Render")

        if isinstance(result, tuple):
            outpath, s3key = result
            job.output_path = outpath
            job.output_s3_key = s3key
        else:
            job.output_path = result

        job.status = models.JobStatus.done
        db.add(job); db.commit(); db.refresh(job)
        return {"ok": True, "output": job.output_path}
    except Exception as e:
        job.status = models.JobStatus.failed
        db.add(job); db.commit()
        raise e
    finally:
        db.close()
