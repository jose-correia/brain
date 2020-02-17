from typing import Optional
from jeec_brain.models.company_dishes import CompanyDishes


class AddCompanyDishService():
    def __init__(self, company_id: int, dish_id: int, dish_quantity: int):
        self.company_id = company_id
        self.dish_id = dish_id
        self.dish_quantity = dish_quantity

    def call(self) -> Optional[CompanyDishes]:
        company_dish = CompanyDishes.create(
            company_id=self.company_id,
            dish_id=self.dish_id,
            dish_quantity=self.dish_quantity
        )
        return company_dish
