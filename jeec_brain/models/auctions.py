from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from jeec_brain.models.companies import Companies
from jeec_brain.models.company_auctions import CompanyAuctions
from sqlalchemy.orm import relationship
from sqlalchemy import sql


class Auctions(ModelMixin, db.Model):
    __tablename__ = 'auctions'
    
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300))

    minimum_value = db.Column(db.Float())
    is_open = db.Column(db.Boolean, default=False)

    bids = relationship("Bids", back_populates='auction', lazy='dynamic', cascade="all,delete")

    participants = relationship("Companies",
        secondary="company_auctions",
        secondaryjoin=sql.and_(CompanyAuctions.company_id == Companies.id))
   
    def __repr__(self):
        return 'Name: {}'.format(self.name)

