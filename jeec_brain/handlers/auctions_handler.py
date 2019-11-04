# SERVICES
from jeec_brain.services.auctions.create_auction_service import CreateAuctionService
from jeec_brain.services.auctions.update_auction_service import UpdateAuctionService
from jeec_brain.services.auctions.delete_auction_service import DeleteAuctionService
from jeec_brain.services.auctions.add_auction_participant_service import AddAuctionParticipantService
from jeec_brain.services.auctions.create_bid_service import CreateBidService


class AuctionsHandler():

    @classmethod
    def create_auction(cls, **kwargs):
        return CreateAuctionService(kwargs=kwargs).call()

    @classmethod
    def update_auction(cls, auction, **kwargs):
        return UpdateAuctionService(auction=auction, kwargs=kwargs).call()

    @classmethod
    def delete_auction(cls, auction):
        return DeleteAuctionService(auction=auction).call()

    @classmethod
    def add_auction_participant(cls, auction, company):
        return AddAuctionParticipantService(auction_id=auction.id, company_id=company.id).call()

    @classmethod
    def create_auction_bid(cls, auction, company, **kwargs):
        return CreateBidService(auction, company, kwargs=kwargs).call()
