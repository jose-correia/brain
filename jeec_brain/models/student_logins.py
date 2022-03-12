from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin


class StudentLogins(db.Model, ModelMixin):
    __tablename__ = "student_logins"

    student_id = db.Column(
        db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), index=True
    )
    date = db.Column(db.String(30))

    def __repr__(self):
        return "Date: {}".format(self.date)
