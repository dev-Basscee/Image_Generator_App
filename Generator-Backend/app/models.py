from sqlalchemy import Column, String, Text, Integer, Float, DateTime
from sqlalchemy.sql import func
from .db import Base
import uuid
import json

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    negative_prompt = Column(Text)
    model = Column(String, default="core")
    aspect_ratio = Column(String, default="1:1")
    steps = Column(Integer, default=0)  # not used by API but kept for future
    guidance = Column(Float, default=0.0)
    status = Column(String, default="queued")  # queued running succeeded failed
    output_key = Column(String)  # s3 object key
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def outputs(self, cdn_base: str | None, bucket: str):
        if not self.output_key:
            return None
        # The API will generate a presigned URL at request time
        return [self.output_key]