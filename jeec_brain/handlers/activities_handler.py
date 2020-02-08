# SERVICES
from jeec_brain.services.activities.create_activity_service import CreateActivityService
from jeec_brain.services.activities.update_activity_service import UpdateActivityService
from jeec_brain.services.activities.delete_activity_service import DeleteActivityService
from jeec_brain.services.activities.add_company_activity_service import AddCompanyActivityService
from jeec_brain.services.activities.update_company_activities_service import UpdateCompanyActivityService
from jeec_brain.services.activities.delete_company_activities_service import DeleteCompanyActivityService
from jeec_brain.services.activities.add_speaker_activity_service import AddSpeakerActivityService
from jeec_brain.services.activities.update_speaker_activities_service import UpdateSpeakerActivityService
from jeec_brain.services.activities.delete_speaker_activities_service import DeleteSpeakerActivityService


class ActivitiesHandler():

    @classmethod
    def create_activity(cls, **kwargs):
        return CreateActivityService(kwargs=kwargs).call()

    @classmethod
    def update_activity(cls, activity, **kwargs):
        return UpdateActivityService(activity=activity, kwargs=kwargs).call()

    @classmethod
    def delete_activity(cls, activity):
        return DeleteActivityService(activity=activity).call()

    @classmethod
    def add_speaker_activity(cls, speaker, activity):
        return AddSpeakerActivityService(speaker.id, activity.id).call()

    @classmethod
    def update_speaker_activity(cls, speaker_activity, speaker, activity):
        return UpdateSpeakerActivityService(speaker_activity, speaker.id, activity.id).call()

    @classmethod
    def delete_speaker_activities(cls, speaker_activity):
        return DeleteSpeakerActivityService(speaker_activity).call()

    @classmethod
    def add_company_activity(cls, company, activity):
        return AddCompanyActivityService(company.id, activity.id).call()

    @classmethod
    def update_company_activity(cls, company_activity, company, activity):
        return UpdateCompanyActivityService(company_activity, company.id, activity.id).call()

    @classmethod
    def delete_company_activities(cls, company_activity):
        return DeleteCompanyActivityService(company_activity).call()