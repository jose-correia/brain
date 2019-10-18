from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin


class Bids(ModelMixin, db.Model):
    __tablename__ = 'bids'
    
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), index=True)
    is_anonymous = db.Column(db.Boolean, default=False)

    value = db.Column(db.Float())
    
    auction = db.relationship('Auctions', back_populates="bids", uselist=False)
    auction_id = db.Column(db.Integer, db.ForeignKey('auctions.id'))
   
    def __repr__(self):
        return 'Value: {}'.format(self.value)

