from typing import List

from pydantic import BaseModel, validator


class VectorMetadata(BaseModel):
    guideline_id: int = -1
    section_id: int = -1
    recommendation_id: int = -1
    pico_id: int = -1
    outcome_id: int = -1
    text: str

    @validator("text", pre=True, always=True)
    def parse_text(cls, value):
        try:
            return str(value)
        except ValueError:
            raise ValueError("Invalid text")


class Vector(BaseModel):
    id: str
    embedding: List[float]
    metadata: VectorMetadata
