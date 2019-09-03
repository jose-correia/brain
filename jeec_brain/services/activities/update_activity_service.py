from typing import Dict, Optional
from jeec_brain.models.activities import Activities


class UpdateActivityService():
    
    def __init__(self, activity: Activities, kwargs: Dict):
        self.activity = activity
        self.kwargs = kwargs

    def call(self) -> Optional[Activities]:
        update_result = self.activity.update(**self.kwargs)
        return update_result
