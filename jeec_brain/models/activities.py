from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.tags import Tags
from jeec_brain.models.activities_tags import ActivitiesTags
from jeec_brain.models.enums.activity_chat_enum import ActivityChatEnum
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class Activities(db.Model, ModelMixin):
    __tablename__ = 'activities'
    
    name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(300))

    location = db.Column(db.String(100), default="Instituto Superior Técnico")
    day = db.Column(db.String(20))
    time = db.Column(db.String(10))
    end_time = db.Column(db.String(10))

    registration_open = db.Column(db.Boolean, default=False)
    registration_link = db.Column(db.String(100))

    activity_type = relationship('ActivityTypes', back_populates="activities", uselist=False)
    activity_type_id = db.Column(db.Integer, db.ForeignKey('activity_types.id'))

    event = relationship('Events', back_populates="activities", uselist=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    chat_id = db.Column(db.String)
    chat_code = db.Column(db.String)
    chat_type = db.Column(db.Enum(ActivityChatEnum))

    zoom_link = db.Column(db.String)

    reward_id = db.Column(db.Integer, db.ForeignKey('rewards.id', ondelete='SET NULL'))
    reward = relationship('Rewards')

    moderator_id = db.Column(db.Integer, db.ForeignKey('speakers.id', ondelete='SET NULL'))
    moderator = relationship('Speakers')

    tags = relationship("Tags",
        secondary="activities_tags",
        secondaryjoin=sql.and_(ActivitiesTags.tag_id == Tags.id))

    points = db.Column(db.Integer())
    quest = db.Column(db.Boolean, default=False)
   
    def __repr__(self):
        return 'Type: {}  |  Name: {}'.format(self.activity_type.name, self.name)
