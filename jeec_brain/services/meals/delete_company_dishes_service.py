from jeec_brain.models.company_dishes import CompanyDishes


class DeleteCompanyDishesService():

    def __init__(self, company_dish: CompanyDishes):
        self.company_dish = company_dish

    def call(self) -> bool:
        result = self.company_dish.delete()
        return result
