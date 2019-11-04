from jeec_brain.models.companies import Companies
from jeec_brain.database import db_session
from sqlalchemy import text

class CompaniesFinder():

    @classmethod
    def get_from_name(cls, name):
        return Companies.query.filter_by(name=name).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Companies.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def search_by_name(cls, name):
        search = "%{}%".format(name)
        return Companies.query.filter(Companies.name.ilike(search)).all()
    
    @classmethod
    def search_by_email(cls, email):
        search = "%{}%".format(email)
        return Companies.query.filter(Companies.email.ilike(search)).all()
        
    @classmethod
    def get_all(cls):
        return Companies.query.order_by(Companies.name).all()
    
    @classmethod
    def get_all_with_cv_access(cls):
        return Companies.query.filter_by(access_cv_platform=True)

    @classmethod
    def get_from_external_id(cls, external_id):
        return Companies.query.filter_by(external_id=external_id).first()
        
    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            companies = Companies.query.filter_by(**kwargs).all()
        except Exception:
            return None
        
        return companies

    @classmethod
    def get_company_auctions(cls, company):
        command = text (
            """
                SELECT
                    auctions.external_id, auctions.name
                FROM
                    auctions
                INNER JOIN
                    company_auctions
                ON
                    company_auctions.company_id=:company_id
                AND 
                    auctions.id=company_auctions.auction_id;"""
        )
        return db_session.execute(command, {"company_id": company.id,}).fetchall()
