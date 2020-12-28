from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class JeecpotRewards(db.Model, ModelMixin):
    __tablename__ = 'jeecpot_rewards'
    
    student_reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))
    student_reward = relationship('Rewards', foreign_keys=student_reward_id)
    student_winner_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    student_winner = relationship('Students', foreign_keys=student_winner_id)

    first_squad_reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))
    first_squad_reward = relationship('Rewards', foreign_keys=first_squad_reward_id)
    first_squad_winner_id = db.Column(db.Integer, db.ForeignKey('squads.id'))
    first_squad_winner = relationship('Squads', foreign_keys=first_squad_winner_id)

    second_squad_reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))
    second_squad_reward = relationship('Rewards', foreign_keys=second_squad_reward_id)
    second_squad_winner_id = db.Column(db.Integer, db.ForeignKey('squads.id'))
    second_squad_winner = relationship('Squads', foreign_keys=second_squad_winner_id)

    third_squad_reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))
    third_squad_reward = relationship('Rewards', foreign_keys=third_squad_reward_id)
    third_squad_winner_id = db.Column(db.Integer, db.ForeignKey('squads.id'))
    third_squad_winner = relationship('Squads', foreign_keys=third_squad_winner_id)

    def __repr__(self):
        return 'Name: {}'.format(self.name)