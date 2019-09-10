from jeec_brain.models.enums.activity_type_enum import ActivityTypeEnum


class GetActivityTypesService():

    def call():
        return dir(ActivityTypeEnum)[4:]
