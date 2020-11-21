from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.activities_tags import ActivitiesTags
from jeec_brain.models.activities import Activities
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class Rewards(db.Model, ModelMixin):
    __tablename__ = 'rewards'
    
    name = db.Column(db.String(100), unique=True, nullable=False)

    description = db.Column(db.String(300))

    link = db.Column(db.String(100))

    quantity = db.Column(db.Integer)

    level = db.Column(db.Integer)

    def __repr__(self):
        return 'Name: {}'.format(self.name)