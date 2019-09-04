from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship


class Speakers(ModelMixin, db.Model):
    __tablename__ = 'speakers'
    
    name = db.Column(db.String(100), unique=True, nullable=False)

    company = db.Column(db.String(100))
    position = db.Column(db.String(100))

    country = db.Column(db.String(100))

    bio = db.Column(db.String(200))

    linkedin_url = db.Column(db.String(100))

    activities = relationship("Activities", back_populates='speaker', lazy='dynamic')
    
    def __repr__(self):
        return 'Name: {}'.format(self.name)
