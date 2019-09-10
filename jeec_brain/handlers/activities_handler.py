# SERVICES
from jeec_brain.services.activities.create_activity_service import CreateActivityService
from jeec_brain.services.activities.update_activity_service import UpdateActivityService
from jeec_brain.services.activities.delete_activity_service import DeleteActivityService
from jeec_brain.services.activities.add_company_activity_service import AddCompanyActivityService
from jeec_brain.services.activities.add_speaker_activity_service import AddSpeakerActivityService


class ActivitiesHandler():

    @classmethod
    def create_activity(cls, **kwargs):
        return CreateActivityService(payload=kwargs).call()

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
    def add_company_activity(cls, company, activity):
        return AddCompanyActivityService(company.id, activity.id).call()
