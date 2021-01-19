from typing import Optional
from jeec_brain.models.company_activities import CompanyActivities


class AddCompanyActivityService():
    def __init__(self, company_id: int, activity_id: int, zoom_link: str):
        self.company_id = company_id
        self.activity_id = activity_id
        self.zoom_link = zoom_link

    def call(self) -> Optional[CompanyActivities]:
        company_activity = CompanyActivities.create(
            company_id=self.company_id,
            activity_id=self.activity_id,
            zoom_link=self.zoom_link
        )
        
        return company_activity
