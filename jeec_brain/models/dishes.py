from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin


class Dishes(ModelMixin, db.Model):
    __tablename__ = 'dishes'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))

    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), index=True)

    def __repr__(self):
        return 'Dish: {}'.format(self.name)
