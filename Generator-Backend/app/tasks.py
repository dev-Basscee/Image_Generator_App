import os
import requests
from celery import Celery
from sqlalchemy.orm import Session
from .db import SessionLocal
from .models import Job
from .storage import put_object

celery = Celery(__name__, broker=os.getenv("REDIS_URL"))

API_KEY = os.getenv("STABILITY_API_KEY")
MODEL = os.getenv("STABILITY_MODEL", "core")  # core or sd3

TXT2IMG_URL = "https://api.stability.ai/v2beta/stable-image/generate/core" if MODEL == "core" else "https://api.stability.ai/v2beta/stable-image/generate/sd3"

@celery.task(name="generate_image")
def generate_image(job_id: str):
    db: Session = SessionLocal()
    job = db.get(Job, job_id)
    if not job:
        return
    job.status = "running"
    db.commit()

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "image/png",
        }
        data = {
            "prompt": job.prompt,
            "output_format": "png",
            "aspect_ratio": job.aspect_ratio,
        }
        r = requests.post(TXT2IMG_URL, headers=headers, files={"none":"none"}, data=data, timeout=120)
        r.raise_for_status()
        img_bytes = r.content

        key = f"jobs/{job.id}/out.png"
        put_object(key, img_bytes, content_type="image/png")

        job.status = "succeeded"
        job.output_key = key
        db.commit()
    except Exception as e:
        job.status = "failed"
        db.commit()
        raise
    finally:
        db.close()