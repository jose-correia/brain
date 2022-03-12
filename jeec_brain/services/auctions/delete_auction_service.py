from jeec_brain.models.auctions import Auctions


class DeleteAuctionService:
    def __init__(self, auction: Auctions):
        self.auction = auction

    def call(self) -> bool:
        result = self.auction.delete()
        return result
