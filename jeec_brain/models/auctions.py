from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship


class Auctions(ModelMixin, db.Model):
    __tablename__ = 'auctions'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))

    minimum_value = db.Column(db.Float())
    bids = relationship("Bids", back_populates='team', lazy='dynamic', cascade="all,delete")

   
    def __repr__(self):
        return 'Name: {}'.format(self.name)

