from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class GenerateRequest(BaseModel):
    brand_name: str = Field(..., min_length=2)
    persona: str = Field(..., min_length=2)
    platform: str = Field(..., min_length=2)
    product_brief: str = Field(..., min_length=3)


class GenerationRecord(BaseModel):
    job_id: str
    brand_name: str
    persona: str
    platform: str
    product_brief: str
    generated_text: str
    enhanced_prompt: str
    image_url: Optional[str] = None
    final_asset_url: Optional[str] = None
    status: str
    created_at: str
    updated_at: str
