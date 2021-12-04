from pydantic import BaseModel, Field
from uuid import UUID

class CompanyPath(BaseModel):
    company_external_id: UUID = Field(..., description="Company external ID")