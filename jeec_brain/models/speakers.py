from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
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

    def __repr__(self):
        return 'Name: {}'.format(self.name)
