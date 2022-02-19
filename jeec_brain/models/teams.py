from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship


class Teams(db.Model, ModelMixin):
    __tablename__ = 'teams'
    
    name = db.Column(db.String(100), unique=False)
    description = db.Column(db.String(300))

    website_priority = db.Column(db.Integer(), default=0) # for sorting the teams in the website
    
    members = relationship("Colaborators", back_populates='team', lazy='dynamic', cascade="all,delete", order_by="Colaborators.name")

    event = relationship('Events', back_populates="teams", uselist=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return 'Name: {}'.format(self.name)
