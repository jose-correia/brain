from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class PersonalRewards(db.Model, ModelMixin):
    __tablename__ = 'personal_rewards'
    
    name = db.Column(db.String(100), unique=True, nullable=False)

    description = db.Column(db.String(300))

    link = db.Column(db.String(100))

    quantity = db.Column(db.Integer)

    level = relationship('Levels')
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'))

    def __repr__(self):
        return 'Name: {}'.format(self.name)