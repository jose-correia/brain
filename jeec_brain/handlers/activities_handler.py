# SERVICES
from jeec_brain.services.activities.create_activity_service import CreateActivityService
from jeec_brain.services.activities.update_activity_service import UpdateActivityService
from jeec_brain.services.activities.delete_activity_service import DeleteActivityService


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

