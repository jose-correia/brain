from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.tags import Tags
from jeec_brain.models.activities_tags import ActivitiesTags
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class Activities(ModelMixin, db.Model):
    __tablename__ = 'activities'
    
    name = db.Column(db.String(100), unique=True, nullable=False)
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

    tags = relationship("Tags",
        secondary="activities_tags",
        secondaryjoin=sql.and_(ActivitiesTags.tag_id == Tags.id))

    points = db.Column(db.Integer())
   
    def __repr__(self):
        return 'Type: {}  |  Name: {}'.format(self.type, self.name)
