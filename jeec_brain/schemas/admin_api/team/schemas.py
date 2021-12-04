from pydantic import BaseModel, Field
from uuid import UUID

class TeamPath(BaseModel):
    team_external_id: UUID = Field(..., description="Team external ID")

class TeamMemberPath(BaseModel):
    team_external_id: UUID = Field(..., description="Team external ID")
    member_external_id: UUID = Field(..., description="Member external ID")