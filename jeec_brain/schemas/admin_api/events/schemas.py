from pydantic import BaseModel, Field
from uuid import UUID


class EventPath(BaseModel):
    event_external_id: UUID = Field(..., description="Event external ID")
