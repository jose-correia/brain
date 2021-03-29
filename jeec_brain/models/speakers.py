from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.activities import Activities
from jeec_brain.models.speaker_activities import SpeakerActivities
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class Speakers(db.Model, ModelMixin):
    __tablename__ = 'speakers'
    
    name = db.Column(db.String(100), unique=True, nullable=False)

    company = db.Column(db.String(100))
    company_link = db.Column(db.String(100))
    position = db.Column(db.String(100))

    country = db.Column(db.String(100))
    bio = db.Column(db.String(300))

    linkedin_url = db.Column(db.String(100))
    youtube_url = db.Column(db.String(100))
    website_url = db.Column(db.String(100))

    spotlight = db.Column(db.Boolean, default=False)

    activities = relationship("Activities",
        secondary="speaker_activities",
        secondaryjoin=sql.and_(SpeakerActivities.activity_id == Activities.id))

    def __repr__(self):
        return 'Name: {}'.format(self.name)
