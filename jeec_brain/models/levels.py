from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship


class Levels(db.Model, ModelMixin):
    __tablename__ = "levels"

    value = db.Column(db.Integer(), unique=True, nullable=False)
    points = db.Column(db.Integer(), nullable=False)

    reward_id = db.Column(db.Integer, db.ForeignKey("rewards.id", ondelete="SET NULL"))
    reward = relationship("Rewards")

    def __repr__(self):
        return "Level: {}".format(self.value)
