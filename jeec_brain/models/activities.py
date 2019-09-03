from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.enums.activity_type_enum import ActivityTypeEnum
from sqlalchemy.dialects.postgresql import TIMESTAMP
from datetime import datetime
from sqlalchemy.orm import relationship


class Activities(ModelMixin, db.Model):
    __tablename__ = 'activities'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))

    location = db.Column(db.String(100), default="Instituto Superior Técnico")
    datetime = db.Column(TIMESTAMP)

    type = db.Column(db.Enum(ActivityTypeEnum), nullable=False)
    
    company = relationship('Companies', back_populates="activities", uselist=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    speaker = relationship('Speakers', back_populates="activities", uselist=False)
    speaker_id = db.Column(db.Integer, db.ForeignKey('speakers.id'))

    registration_open = db.Column(db.Boolean, default=False)
    registration_link = db.Column(db.String(100))

   
    def __repr__(self):
        return 'Username: {}  |  Name: {}'.format(self.username, self.name)

    def open_registration(self):
        self.registration_open = True
