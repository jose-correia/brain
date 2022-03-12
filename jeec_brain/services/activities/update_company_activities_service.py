from typing import Dict, Optional
from jeec_brain.models.company_activities import CompanyActivities


class UpdateCompanyActivityService:
    def __init__(
        self, company_activity: CompanyActivities, company_id: int, activity_id: int
    ):
        self.company_activity = company_activity
        self.company_id = company_id
        self.activity_id = activity_id

    def call(self) -> Optional[CompanyActivities]:
        update_result = self.company_activity.update(
            company_id=self.company_id, activity_id=self.activity_id
        )
        return update_result
