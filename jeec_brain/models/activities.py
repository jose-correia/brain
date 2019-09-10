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
    day = db.Column(db.String(20))
    time = db.Column(db.String(10))

    type = db.Column(db.Enum(ActivityTypeEnum), nullable=False)

    registration_open = db.Column(db.Boolean, default=False)
    registration_link = db.Column(db.String(100))
   
    def __repr__(self):
        return 'Type: {}  |  Name: {}'.format(self.type, self.name)

    def open_registration(self):
        self.registration_open = True
