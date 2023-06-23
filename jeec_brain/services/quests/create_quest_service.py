from jeec_brain.models.quests import Quests
from typing import Dict,Optional


class CreateQuestService:
    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Quests]:

        quest = Quests.create(**self.kwargs)

        if not quest:
            return None

        return quest

