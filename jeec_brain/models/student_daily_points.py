from jeec_brain.database import db
from sqlalchemy.orm import relationship
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.students import Students


class StudentDailyPoints(db.Model, ModelMixin):
    __tablename__ = "student_daily_points"

    student_id = db.Column(
        db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), index=True
    )
    student = relationship("Students")

    date = db.Column(db.String(30))
    points = db.Column(db.Integer())

    def __repr__(self):
        return "Date: {} Points: {}".format(self.date, self.points)
