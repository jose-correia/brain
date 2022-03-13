from typing import Dict, Optional
from jeec_brain.models.company_meals import CompanyMeals


class UpdateCompanyMealsService:
    def __init__(self, company_meal: CompanyMeals, company_id: int, meal_id: int):
        self.company_meal = company_meal
        self.company_id = company_id
        self.meal_id = meal_id

    def call(self) -> Optional[CompanyMeals]:
        update_result = self.company_meal.update(
            company_id=self.company_id, meal_id=self.meal_id
        )
        return update_result
