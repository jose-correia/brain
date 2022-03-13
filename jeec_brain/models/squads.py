from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship


class Squads(db.Model, ModelMixin):
    __tablename__ = "squads"

    name = db.Column(db.String(100), unique=True, nullable=False)
    cry = db.Column(db.String(100))

    members = relationship(
        "Students",
        back_populates="squad",
        lazy="dynamic",
        order_by="Students.total_points",
    )

    captain_ist_id = db.Column(db.String(10), unique=True, nullable=False)

    daily_points = db.Column(db.Integer, default=0)
    total_points = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "Name: {}".format(self.name)
