# SERVICES
from jeec_brain.services.activity_types.create_activity_type_service import (
    CreateActivityTypeService,
)
from jeec_brain.services.activity_types.update_activity_type_service import (
    UpdateActivityTypeService,
)
from jeec_brain.services.activity_types.delete_activity_type_service import (
    DeleteActivityTypeService,
)


class ActivityTypesHandler:
    @classmethod
    def create_activity_type(cls, event, **kwargs):
        return CreateActivityTypeService(event=event, kwargs=kwargs).call()

    @classmethod
    def update_activity_type(cls, activity_type, **kwargs):
        return UpdateActivityTypeService(
            activity_type=activity_type, kwargs=kwargs
        ).call()

    @classmethod
    def delete_activity_type(cls, activity_type):
        return DeleteActivityTypeService(activity_type=activity_type).call()
