from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship


class Colaborators(db.Model, ModelMixin):
    __tablename__ = 'colaborators'
    
    name = db.Column(db.String(100), unique=True, nullable=False)
    ist_id = db.Column(db.String(10))
    email = db.Column(db.String(100))

    team = relationship('Teams', back_populates="members", uselist=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    linkedin_url = db.Column(db.String(150))

    def __repr__(self):
        return 'Name: {} | Team: {}'.format(self.name, self.team)
