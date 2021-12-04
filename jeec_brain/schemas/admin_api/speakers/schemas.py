from pydantic import BaseModel, Field
from uuid import UUID

class SpeakerPath(BaseModel):
    speaker_external_id: UUID = Field(..., description="Speaker external ID")