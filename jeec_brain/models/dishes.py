from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.enums.dish_type_enum import DishTypeEnum


class Dishes(db.Model, ModelMixin):
    __tablename__ = "dishes"

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))
    type = db.Column(db.Enum(DishTypeEnum), nullable=False)

    meal_id = db.Column(
        db.Integer, db.ForeignKey("meals.id", ondelete="CASCADE"), index=True
    )

    def __repr__(self):
        return "Dish: {}".format(self.name)
