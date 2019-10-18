from jeec_brain.models.bids import Bids
from jeec_brain.models.auctions import Auctions
from jeec_brain.models.enums.activity_type_enum import ActivityTypeEnum


class AuctionsFinder():

    @classmethod
    def get_all(cls):
        return Auctions.query().order_by(Auctions.name).all()

    @classmethod
    def get_auction_by_external_id(cls, external_id):
        return Auctions.query().filter_by(external_id=external_id).first()

    @classmethod
    def get_auction_by_name(cls, name):
        return Auctions.query().filter_by(name=name).first()

    @classmethod
    def get_auction_highest_bid(cls, auction):
        return Bids.query().filter_by(auction_id=auction.id).order_by(Bids.value.desc())

    @classmethod
    def get_company_bids(cls, auction, company):
        return Bids.query().filter_by(auction_id=auction.id, company_id=company.id).order_by(Bids.value.desc())
