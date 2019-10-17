from typing import Dict, Optional
from jeec_brain.models.auctions import Auctions


class UpdateAuctionService():
    
    def __init__(self, auction: Auctions, kwargs: Dict):
        self.auction = auction
        self.kwargs = kwargs

    def call(self) -> Optional[Auctions]:
        update_result = self.auction.update(**self.kwargs)
        return update_result
