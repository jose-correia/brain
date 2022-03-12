from pydantic import BaseModel, Field
from uuid import UUID


class MealPath(BaseModel):
    meal_external_id: UUID = Field(..., description="Meal external ID")
