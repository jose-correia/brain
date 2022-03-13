from typing import Optional
from jeec_brain.models.company_meals import CompanyMeals


class AddCompanyMealService:
    def __init__(self, company_id: int, meal_id: int, max_dish_quantity: int):
        self.company_id = company_id
        self.meal_id = meal_id
        self.max_dish_quantity = max_dish_quantity

    def call(self) -> Optional[CompanyMeals]:
        company_meal = CompanyMeals.create(
            company_id=self.company_id,
            meal_id=self.meal_id,
            max_dish_quantity=self.max_dish_quantity,
        )
        return company_meal
