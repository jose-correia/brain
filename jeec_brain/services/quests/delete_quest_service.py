from jeec_brain.models.quests import Quests

class DeleteQuestService:
    def __init__(self, quest: Quests):
        self.quest = quest

    def call(self) -> bool:
        result = self.quest.delete()
        return result
