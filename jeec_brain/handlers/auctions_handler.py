# SERVICES
from jeec_brain.services.auctions.create_auction_service import CreateAuctionService
from jeec_brain.services.auctions.update_auction_service import UpdateAuctionService
from jeec_brain.services.auctions.delete_auction_service import DeleteAuctionService
from jeec_brain.services.auctions.add_auction_participant_service import (
    AddAuctionParticipantService,
)
from jeec_brain.services.auctions.create_bid_service import CreateBidService
from jeec_brain.services.mail.send_mail_service import SendMailService


class AuctionsHandler:
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
        return AddAuctionParticipantService(
            auction_id=auction.id, company_id=company.id
        ).call()

    @classmethod
    def create_auction_bid(cls, auction, company_user, **kwargs):
        return CreateBidService(auction, company_user, kwargs=kwargs).call()

    @classmethod
    def send_bid_update_email(cls, company_users, auction, value):
        subject = f"{auction.name} - New highest bidder"
        paragrah = "<br>"
        for company_user in company_users:
            company_name = company_user.company.name
            company_name = (
                company_name + "'"
                if company_name[-1] in ["S", "s"]
                else company_name + "'s"
            )
            content = f"Hello {company_user.user.name},{paragrah*2}{company_name} bid in {auction.name} has just been surpassed.{paragrah}A bid of {value}€ was submitted!{paragrah*2}Kind regards,{paragrah}JEEC Team"
            SendMailService([company_user.user.email], subject, content).call()
