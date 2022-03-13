from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy import Column, Integer, ForeignKey


class CompanyMeals(db.Model, ModelMixin):
    __tablename__ = "company_meals"

    company_id = Column(
        Integer, ForeignKey("companies.id", ondelete="CASCADE"), index=True
    )
    meal_id = Column(Integer, ForeignKey("meals.id", ondelete="CASCADE"), index=True)

    max_dish_quantity = Column(Integer)
