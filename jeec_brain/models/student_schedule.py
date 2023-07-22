from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin

from sqlalchemy.orm import relationship
from sqlalchemy import sql

class ScheduleStudent(db.Model, ModelMixin):
    __tablename__ = "schedule_student"

    student_id = db.Column(db.String(100), unique=False, nullable=False)
    classes = db.Column(db.String())
    activities = db.Column(db.String())
    showFenix = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return "Type: {}  |  Name: {}".format(self.student_id, self.classes, self.activities)