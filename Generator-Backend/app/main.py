import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import Job
from .schemas import CreateJob, JobOut
from .auth import require_api_key
from .tasks import generate_image
from .storage import presigned_url
from .middleware import add_cors

app = FastAPI(title="Image Generator API")
add_cors(app)

# Create tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.post("/v1/generations", response_model=JobOut)
def create_job(body: CreateJob, user=Depends(require_api_key), db: Session = Depends(get_db)):
    job = Job(
        user_id=user.id,
        prompt=body.prompt,
        negative_prompt=body.negative_prompt,
        aspect_ratio=body.aspect_ratio,
        model=body.model,
    )
    db.add(job)
    db.commit()
    generate_image.delay(job.id)
    return JobOut(id=job.id, status=job.status)

@app.get("/v1/generations/{job_id}", response_model=JobOut)
def get_job(job_id: str, user=Depends(require_api_key), db: Session = Depends(get_db)):
    job = db.get(Job, job_id)
    if not job or job.user_id != user.id:
        raise HTTPException(404, "Not found")
    urls = None
    if job.output_key and job.status == "succeeded":
        urls = [presigned_url(job.output_key, 3600)]
    return JobOut(id=job.id, status=job.status, output_urls=urls)

@app.get("/healthz")
def healthz():
    return JSONResponse({"ok": True})