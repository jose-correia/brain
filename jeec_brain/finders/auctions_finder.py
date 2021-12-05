from jeec_brain.models.bids import Bids
from jeec_brain.models.auctions import Auctions
from jeec_brain.models.company_auctions import CompanyAuctions
from jeec_brain.models.companies import Companies
from jeec_brain.models.company_users import CompanyUsers
from jeec_brain.database import db_session
from sqlalchemy import text


class AuctionsFinder():

    @classmethod
    def get_all(cls):
        return Auctions.query.order_by(Auctions.name).all()

    @classmethod
    def get_auction_by_external_id(cls, external_id):
        return Auctions.query.filter_by(external_id=external_id).first()

    @classmethod
    def get_auction_by_name(cls, name):
        return Auctions.query.filter_by(name=name).first()

    @classmethod
    def get_auction_highest_bid(cls, auction):
        return Bids.query.filter_by(auction_id=auction.id).order_by(Bids.value.desc()).first()

    @classmethod
    def get_auction_company_with_bid(cls, auction, bid):
        return Companies.query.filter((Auctions.id==auction.id) & (Bids.auction_id==auction.id) & (Bids.id==bid.id) & (Companies.id==bid.company_id)).first()

    @classmethod
    def get_company_bids_from_user(cls, auction, company_user):
        company_user_ids = [user.id for user in company_user.company.users]
        return Bids.query.filter_by(auction_id=auction.id).filter(Bids.company_user_id.in_(company_user_ids)).order_by(Bids.value.desc())

    @classmethod
    def get_company_users_from_auction(cls, company, auction):
        return CompanyUsers.query.filter(CompanyUsers.id == Bids.company_user_id, CompanyUsers.company_id == company.id, Bids.auction_id == auction.id).all()

    @classmethod
    def get_not_participants(cls, auction):
        command = text (
            """
                SELECT
                    *
                FROM
                    companies as c
                WHERE
                    c.id 
                NOT IN (
                    SELECT
                        c2.id
                    FROM
                        companies as c2
                    INNER JOIN
                        company_auctions as c_auc2
                    ON
                        c2.id = c_auc2.company_id
                    AND
                        c_auc2.auction_id=:auction_id
                );"""
        )
        return db_session.execute(command, {"auction_id": auction.id,}).fetchall()
