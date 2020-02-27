from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy import Column, Integer, ForeignKey


class CompanyDishes(db.Model, ModelMixin):
    __tablename__ = 'company_dishes'

    company_id = Column(Integer, ForeignKey('companies.id'), index=True)
    dish_id = Column(Integer, ForeignKey('dishes.id'), index=True)

    dish_quantity = Column(Integer)