from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.enums.meal_type_enum import MealTypeEnum


class Meals(db.Model, ModelMixin):
    __tablename__ = "meals"

    location = db.Column(db.String(100), default="Instituto Superior Técnico")
    day = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(10))

    registration_day = db.Column(db.String(20), nullable=False)
    registration_time = db.Column(db.String(10))

    type = db.Column(db.Enum(MealTypeEnum), nullable=False)

    def __repr__(self):
        return "Meal: {} | Day: {}".format(self.type.name, self.day)
