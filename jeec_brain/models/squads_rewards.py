from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class SquadsRewards(db.Model, ModelMixin):
    __tablename__ = 'squads_rewards'
    
    reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))
    reward = relationship('Rewards')

    date = db.Column(db.String(30), unique=True)

    winner = relationship('Squads')
    winner_id = db.Column(db.Integer, db.ForeignKey('squads.id'))

    def __repr__(self):
        return 'Name: {}'.format(self.name)