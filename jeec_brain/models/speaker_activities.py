from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy import Column, Integer, ForeignKey


class SpeakerActivities(db.Model, ModelMixin):
    __tablename__ = 'speaker_activities'

    speaker_id = Column(Integer, ForeignKey('speakers.id', ondelete='CASCADE'), index=True)
    activity_id = Column(Integer, ForeignKey('activities.id', ondelete='CASCADE'), index=True)
