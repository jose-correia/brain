from typing import Optional
from jeec_brain.models.company_dishes import CompanyDishes


class AddCompanyDishService():
    def __init__(self, company_id: int, dish_id: int):
        self.company_id = company_id
        self.dish_id = dish_id

    def call(self) -> Optional[CompanyDishes]:
        company_dish = CompanyDishes.create(
            company_id=self.company_id,
            dish_id=self.dish_id
        )
        return company_dish
