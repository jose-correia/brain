# SERVICES
from jeec_brain.services.quests.create_quest_service import CreateQuestService
from jeec_brain.services.quests.update_quest_service import UpdateQuestService
from jeec_brain.services.quests.delete_quest_service import DeleteQuestService

class QuestsHandler:
    @classmethod
    def create_quest(cls, **kwargs):
        return CreateQuestService(kwargs=kwargs).call()

    @classmethod
    def update_quest(cls, quest, **kwargs):
        return UpdateQuestService(quest, kwargs).call()

    @classmethod
    def delete_quest(cls, quest):
        return DeleteQuestService(quest).call()

