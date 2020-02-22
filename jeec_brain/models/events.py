from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship


class Events(ModelMixin, db.Model):
    __tablename__ = 'events'
    
    name = db.Column(db.String(100), nullable=False)

    start_date = db.Column(db.String(30))
    end_date = db.Column(db.String(30))

    default = db.Column(db.Boolean, default=False)

    email = db.Column(db.String(100))
    location = db.Column(db.String(100))

    facebook_link = db.Column(db.String(100))
    facebook_event_link = db.Column(db.String(100))
    youtube_link = db.Column(db.String(100))
    instagram_link = db.Column(db.String(100))

    activity_types = relationship("ActivityTypes", back_populates='event', lazy='dynamic', cascade="all,delete")
    activities = relationship("Activities", back_populates='event', lazy='dynamic', cascade="all,delete")

    def __repr__(self):
        return 'Name: {} | date: {}'.format(self.name, self.start_date)
