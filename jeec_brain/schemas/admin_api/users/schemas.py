from pydantic import BaseModel, Field
from uuid import UUID


class UserPath(BaseModel):
    user_external_id: UUID = Field(..., description="User external ID")
