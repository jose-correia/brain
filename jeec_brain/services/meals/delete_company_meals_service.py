from jeec_brain.models.company_meals import CompanyMeals


class DeleteCompanyMealsService():

    def __init__(self, company_meal: CompanyMeals):
        self.company_meal = company_meal

    def call(self) -> bool:
        result = self.company_meal.delete()
        return result
