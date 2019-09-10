from typing import Optional
from jeec_brain.models.company_activities import CompanyActivities


class AddCompanyActivityService():
    def __init__(self, company_id: int, activity_id: int):
        self.company_id = company_id
        self.activity_id = activity_id

    def call(self) -> Optional[CompanyActivities]:
        company_activity = CompanyActivities.create(
            company_id=self.company_id,
            activity_id=self.activity_id
        )
        return company_activity
