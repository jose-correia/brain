from jeec_brain.database import db
from sqlalchemy.orm import relationship
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.squads import Squads


class SquadDailyPoints(db.Model, ModelMixin):
    __tablename__ = 'squad_daily_points'

    squad_id = db.Column(db.Integer, db.ForeignKey('squads.id', ondelete='CASCADE'), index=True)
    squad = relationship('Squads')

    date = db.Column(db.String(30))
    points = db.Column(db.Integer())

    def __repr__(self):
        return 'Date: {} Points: {}'.format(self.date, self.points)