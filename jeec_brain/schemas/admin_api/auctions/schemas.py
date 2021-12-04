from pydantic import BaseModel, Field
from uuid import UUID

class AuctionPath(BaseModel):
    auction_external_id: UUID = Field(..., description="Auction external ID")