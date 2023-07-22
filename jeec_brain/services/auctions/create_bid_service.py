import logging
from jeec_brain.models.auctions import Auctions
from jeec_brain.models.company_users import CompanyUsers
from jeec_brain.models.bids import Bids
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateBidService:
    def __init__(self, auction: Auctions, company_user: CompanyUsers, kwargs: Dict):
        self.auction = auction
        self.company_user = company_user
        self.kwargs = kwargs

    def call(self) -> Optional[Bids]:

        bid = Bids.create(
            auction_id=self.auction.id,
            company_user_id=self.company_user.id,
            **self.kwargs
        )

        if not bid:
            return None

        try:
            # add new bid to the auction
            self.auction.bids.append(bid)
            self.auction.save()
        except Exception:
            logger.exception("Failed to add new bid to auction")
            return None

        return bid
