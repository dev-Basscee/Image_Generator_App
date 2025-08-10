from pydantic import BaseModel, Field

class CreateJob(BaseModel):
    prompt: str = Field(min_length=3, max_length=800)
    negative_prompt: str | None = None
    aspect_ratio: str = Field(default="1:1", pattern=r"^(1:1|16:9|9:16|4:3|3:2)$")
    model: str = Field(default="core")

class JobOut(BaseModel):
    id: str
    status: str
    output_urls: list[str] | None = None