from jeec_brain.models.company_users import CompanyUsers
from jeec_brain.database import db


class DeleteCompanyUserService():

    def __init__(self, company_user: CompanyUsers):
        self.company_user = company_user

    def call(self) -> bool:

        try:
            db.session.delete(self.company_user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False

        return True
