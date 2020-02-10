from jeec_brain.models.company_activities import CompanyActivities


class DeleteCompanyActivityService():

    def __init__(self, company_activity: CompanyActivities):
        self.company_activity = company_activity

    def call(self) -> bool:
        result = self.company_activity.delete()
        return result
