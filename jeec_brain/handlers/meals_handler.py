# SERVICES
from jeec_brain.services.meals.add_company_dish_service import AddCompanyDishService
from jeec_brain.services.meals.add_company_meal_service import AddCompanyMealService
from jeec_brain.services.meals.create_dish_service import CreateDishService
from jeec_brain.services.meals.create_meal_service import CreateMealService
from jeec_brain.services.meals.delete_company_meals_service import DeleteCompanyMealsService
from jeec_brain.services.meals.delete_dish_service import DeleteDishService
from jeec_brain.services.meals.delete_meal_service import DeleteMealService
from jeec_brain.services.meals.update_company_meals_service import UpdateCompanyMealsService
from jeec_brain.services.meals.update_meal_service import UpdateMealService
from jeec_brain.services.meals.delete_company_dishes_service import DeleteCompanyDishesService


class MealsHandler():

    @classmethod
    def add_company_meal(cls, company, meal, max_dish_quantity):
        return AddCompanyMealService(company.id, meal.id, max_dish_quantity).call()

    @classmethod
    def add_company_dish(cls, company, dish):
        return AddCompanyDishService(company.id, dish.id).call()

    @classmethod
    def create_dish(cls, **kwargs):
        return CreateDishService(kwargs=kwargs).call()

    @classmethod
    def create_meal(cls, **kwargs):
        return CreateMealService(kwargs=kwargs).call()

    @classmethod
    def delete_company_meal(cls, company_meal):
        return DeleteCompanyMealsService(company_meal).call()

    @classmethod
    def delete_company_dish(cls, company_dish):
        return DeleteCompanyDishesService(company_dish).call()

    @classmethod
    def delete_dish(cls, dish):
        return DeleteDishService(dish).call()

    @classmethod
    def delete_meal(cls, meal):
        return DeleteMealService(meal).call()

    @classmethod
    def update_company_meal(cls, company_meal, company, meal):
        return UpdateCompanyMealsService(company_meal, company.id, meal.id).call()

    @classmethod
    def update_meal(cls, meal, **kwargs):
        return UpdateMealService(meal, kwargs).call()
