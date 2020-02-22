from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import relationship


class Activities(ModelMixin, db.Model):
    __tablename__ = 'activities'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))

    location = db.Column(db.String(100), default="Instituto Superior Técnico")
    day = db.Column(db.String(20))
    time = db.Column(db.String(10))

    registration_open = db.Column(db.Boolean, default=False)
    registration_link = db.Column(db.String(100))

    activity_type = relationship('ActivityTypes', back_populates="activities", uselist=False)
    activity_type_id = db.Column(db.Integer, db.ForeignKey('activity_types.id'))

    event = relationship('Events', back_populates="activities", uselist=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
   
    def __repr__(self):
        return 'Type: {}  |  Name: {}'.format(self.type, self.name)
