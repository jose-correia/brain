from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin


class Levels(ModelMixin, db.Model):
    __tablename__ = 'levels'
    
    value = db.Column(db.Integer(), unique=True, nullable=False)
    points = db.Column(db.Integer(), nullable=False)
    
    def __repr__(self):
        return 'Level: {}'.format(self.value)
