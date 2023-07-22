from typing import Dict, Optional
from jeec_brain.models.quests import Quests

class UpdateQuestService:
    def __init__(self, quest: Quests, kwargs: Dict):
        self.quest = quest
        self.kwargs = kwargs

    def call(self) -> Optional[Quests]:
        try:
            update_result = self.quest.update(**self.kwargs)
        except:
            return None

        return update_result
