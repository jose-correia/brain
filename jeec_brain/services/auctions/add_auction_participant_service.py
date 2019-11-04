from typing import Optional
from jeec_brain.models.company_auctions import CompanyAuctions


class AddAuctionParticipantService():
    def __init__(self, company_id: int, auction_id: int):
        self.company_id = company_id
        self.auction_id = auction_id

    def call(self) -> Optional[CompanyAuctions]:
        company_auction = CompanyAuctions.create(
            company_id=self.company_id,
            auction_id=self.auction_id
        )
        return company_auction
