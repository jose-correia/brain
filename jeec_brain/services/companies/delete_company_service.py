from jeec_brain.models.companies import Companies
from jeec_brain.database import db


class DeleteCompanyService():

    def __init__(self, company: Companies):
        self.company = company

    def call(self) -> bool:

        try:
            db.session.delete(self.company)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False

        return True
