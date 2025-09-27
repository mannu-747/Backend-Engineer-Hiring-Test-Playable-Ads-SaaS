
import os
from celery import Celery
from dotenv import load_dotenv
load_dotenv()

broker = os.getenv("CELERY_BROKER", "redis://localhost:6379/0")
celery_app = Celery("worker", broker=broker, backend=broker)
celery_app.conf.task_routes = {"app.workers.tasks.*": {"queue": "renders"}}
