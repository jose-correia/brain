from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class JeecpotRewards(db.Model, ModelMixin):
    __tablename__ = 'jeecpot_rewards'
    
    first_student_reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))
    first_student_reward = relationship('Rewards', foreign_keys=first_student_reward_id)
    first_student_winner_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    first_student_winner = relationship('Students', foreign_keys=first_student_winner_id)

    second_student_reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))
    second_student_reward = relationship('Rewards', foreign_keys=second_student_reward_id)
    second_student_winner_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    second_student_winner = relationship('Students', foreign_keys=second_student_winner_id)

    third_student_reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))
    third_student_reward = relationship('Rewards', foreign_keys=third_student_reward_id)
    third_student_winner_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    third_student_winner = relationship('Students', foreign_keys=third_student_winner_id)

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

    king_job_fair_reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))
    king_job_fair_reward = relationship('Rewards', foreign_keys=king_job_fair_reward_id)
    king_job_fair_winner_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    king_job_fair_winner = relationship('Students', foreign_keys=king_job_fair_winner_id)

    king_knowledge_reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))
    king_knowledge_reward = relationship('Rewards', foreign_keys=king_knowledge_reward_id)
    king_knowledge_winner_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    king_knowledge_winner = relationship('Students', foreign_keys=king_knowledge_winner_id)

    king_hacking_reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))
    king_hacking_reward = relationship('Rewards', foreign_keys=king_hacking_reward_id)
    king_hacking_winner_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    king_hacking_winner = relationship('Students', foreign_keys=king_hacking_winner_id)

    king_networking_reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id'))
    king_networking_reward = relationship('Rewards', foreign_keys=king_networking_reward_id)
    king_networking_winner_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    king_networking_winner = relationship('Students', foreign_keys=king_networking_winner_id)

    def __repr__(self):
        return 'Name: {}'.format(self.name)