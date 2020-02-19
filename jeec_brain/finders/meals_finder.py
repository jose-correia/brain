from jeec_brain.models.meals import Meals
from jeec_brain.models.company_meals import CompanyMeals
from jeec_brain.models.dishes import Dishes
from jeec_brain.models.company_dishes import CompanyDishes
from jeec_brain.models.companies import Companies
from jeec_brain.database import db_session
from sqlalchemy import text


class MealsFinder():

    @classmethod
    def get_meal_from_external_id(cls, external_id):
        return Meals.query().filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all_meals(cls):
        return Meals.query().order_by(Meals.updated_at).all()

    @classmethod
    def get_meals_from_day(cls, day):
        return Meals.query().filter(Meals.day.ilike(day)).order_by(Meals.updated_at).all()

    @classmethod
    def get_meals_from_parameters(cls, kwargs):
        try:
            return Meals.query().filter_by(**kwargs).all()
        except Exception:
            return None
    
    @classmethod
    def get_company_meals_from_meal_id(cls, external_id):
        return CompanyMeals.query.join(Meals, Meals.id == CompanyMeals.meal_id).filter(Meals.external_id == external_id).all()

    @classmethod
    def get_company_meals_from_meal_id_and_company_id(cls, meal_id, company_id):
        return CompanyMeals.query.filter(CompanyMeals.meal_id == meal_id).filter(CompanyMeals.company_id == company_id).first()

    @classmethod
    def get_companies_from_meal_id(cls, meal_id):
        return Companies.query.join(CompanyMeals, CompanyMeals.company_id == Companies.id).filter(CompanyMeals.meal_id == meal_id).all()

    @classmethod
    def get_company_dishes_from_meal_id_and_company_id(cls, meal_id, company_id):
        return CompanyDishes.query.join(Dishes, CompanyDishes.dish_id == Dishes.id).filter(Dishes.meal_id == meal_id).filter(CompanyDishes.company_id == company_id).all()

    @classmethod
    def get_company_dishes_from_meal_id(cls, meal_id):
        return CompanyDishes.join(Dishes, Dishes.id == CompanyDishes.dish_id).filter(Dishes.meal_id == meal_id)
    
    @classmethod
    def get_company_dishes_from_dish_id(cls, dish_id):
        return CompanyDishes.query.filter(CompanyDishes.dish_id == dish_id)
    
    @classmethod
    def get_dishes_from_meal_id(cls, external_id):
        return Dishes.query().join(Meals, Meals.id == Dishes.meal_id).filter(Meals.external_id == external_id).all()

    @classmethod
    def get_dishes_from_dish_external_id(cls, external_id):
        return Dishes.query().filter_by(external_id=external_id).first()

    @classmethod
    def get_dishes_per_company_from_meal_id(cls, meal_id):
        command = text (
            """
                SELECT c.name, d.name, SUM(cd.dish_quantity) as number_of_dishes
                FROM companies as c, dishes as d, company_dishes as cd
                WHERE c.id = cd.company_id AND d.id = cd.dish_id AND d.meal_id=:meal_id
                GROUP BY c.name, d.name
                ORDER BY c.name, d.name;"""
        )
        return db_session.execute(command, {"meal_id": meal_id,}).fetchall()