from typing import Dict, Optional
from jeec_brain.models.company_users import CompanyUsers


class UpdateCompanyUserService():
    
    def __init__(self, company_user: CompanyUsers, kwargs: Dict):
        self.company_user = company_user
        self.kwargs = kwargs

    def call(self) -> Optional[CompanyUsers]:
        try:
            update_result = self.company_user.update(**self.kwargs)
        except:
            return None
            
        return update_result
