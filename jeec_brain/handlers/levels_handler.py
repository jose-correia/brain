# SERVICES
from jeec_brain.services.levels.create_level_service import CreateLevelService
from jeec_brain.services.levels.update_level_service import UpdateLevelService
from jeec_brain.services.levels.delete_level_service import DeleteLevelService

class LevelsHandler():

    @classmethod
    def create_level(cls, **kwargs):
        return CreateLevelService(kwargs=kwargs).call()

    @classmethod
    def update_level(cls, level, **kwargs):
        return UpdateLevelService(level, kwargs)

    @classmethod
    def delete_level(cls, level):
        return DeleteLevelService(level).call()