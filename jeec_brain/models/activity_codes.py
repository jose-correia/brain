from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship


class ActivityCodes(db.Model, ModelMixin):
    __tablename__ = "activity_codes"

    code = db.Column(db.String(16), unique=True, nullable=False, index=True)

    activity = relationship("Activities")
    activity_id = db.Column(
        db.Integer, db.ForeignKey("activities.id", ondelete="CASCADE")
    )

    def __repr__(self):
        return "Code: {}".format(self.code)
