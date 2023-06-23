from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin


class Quests(db.Model, ModelMixin):
    __tablename__ = "quests"

    name =  db.Column(
        db.String()
    )

    description = db.Column(
        db.String()
    )

    reward_id = db.Column(
        db.Integer, db.ForeignKey("rewards.id", ondelete="CASCADE"), index=True
    )
    activities_id = db.Column(
        db.ARRAY(db.Integer)
    )
    activity_type_id = db.Column(
        db.Integer()
    )
    day = db.Column(
        db.String
    )
    number_of_activities =  db.Column(
        db.Integer()
    )
    

    def __repr__(self):
        return "Reward_id:{}, Activities_id:{}, Number of Activities".format(self.reward_id, self.activities_id, self.number_of_activities)