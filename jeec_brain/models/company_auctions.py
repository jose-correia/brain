from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy import Column, Integer, ForeignKey


class CompanyAuctions(db.Model, ModelMixin):
    __tablename__ = 'company_auctions'

    company_id = Column(Integer, ForeignKey('companies.id', ondelete='CASCADE'), index=True)
    auction_id = Column(Integer, ForeignKey('auctions.id', ondelete='CASCADE'), index=True)
