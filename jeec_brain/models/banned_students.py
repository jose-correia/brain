from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin


class BannedStudents(db.Model, ModelMixin):
    __tablename__ = "banned_students"

    name = db.Column(db.String(100), unique=True, nullable=False)
    ist_id = db.Column(db.String(10), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100))

    def __repr__(self):
        return "Name: {}  |  IST id: {}".format(self.name, self.ist_id)
