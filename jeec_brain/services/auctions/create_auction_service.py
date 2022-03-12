import logging
from jeec_brain.models.auctions import Auctions
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateAuctionService:
    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Auctions]:

        auction = Auctions.create(**self.kwargs)

        if not auction:
            return None

        return auction
