from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship


class Squads(db.Model, ModelMixin):
    __tablename__ = 'squads'
    
    name = db.Column(db.String(100), unique=True)
    
    members = relationship("Students", back_populates='squad', lazy='dynamic', cascade="all,delete", order_by="Students.name")

    daily_points = db.Column(db.Integer)
    total_points = db.Column(db.Integer)

    def __repr__(self):
        return 'Name: {}'.format(self.name)