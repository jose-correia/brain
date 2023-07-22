from jeec_brain.database import db
from sqlalchemy.orm import relationship, deferred
from sqlalchemy import sql
from jeec_brain.models.model_mixin import ModelMixin

class StudentRewards(db.Model,ModelMixin):
    __tablename__ = "student_rewards"

    student_id = db.Column(
        db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), index=True
    )
    

    reward_id = db.Column(db.Integer, db.ForeignKey("rewards.id", ondelete="SET NULL"))
    reward = relationship("Rewards")

    acquired = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "Student: {} |   Reward ID: {} | Acquired: {}".format(self.student_id, self.reward_id, self.acquired)
