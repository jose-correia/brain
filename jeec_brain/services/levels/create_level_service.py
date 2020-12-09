import logging
from jeec_brain.models.levels import Levels
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateLevelService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Levels]:
        
        level = Levels.create(**self.kwargs)

        if not level:
            return None

        return level

