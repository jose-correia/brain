from typing import Dict, Optional
from jeec_brain.models.levels import Levels


class UpdateLevelService():
    
    def __init__(self, level: Levels, kwargs: Dict):
        self.level = level
        self.kwargs = kwargs

    def call(self) -> Optional[Levels]:
        try:
            update_result = self.level.update(**self.kwargs)
        except:
            return None
            
        return update_result
