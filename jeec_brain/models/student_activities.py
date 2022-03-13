from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin


class StudentActivities(db.Model, ModelMixin):
    __tablename__ = "student_activities"

    __table_args__ = (
        db.UniqueConstraint("student_id", "activity_id", name="uix_student_activities"),
    )

    student_id = db.Column(
        db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), index=True
    )
    activity_id = db.Column(
        db.Integer, db.ForeignKey("activities.id", ondelete="CASCADE"), index=True
    )
    code = db.Column(db.String(16), nullable=False)
