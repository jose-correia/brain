from pydantic import BaseModel, Field
from uuid import UUID

class StudentPath(BaseModel):
    student_external_id: UUID = Field(..., description="Student external ID")