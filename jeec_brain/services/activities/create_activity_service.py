import logging
from jeec_brain.models.activities import Activities
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateActivityService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Activities]:
        
        activity = Activities.create(**self.kwargs)

        if not activity:
            return None

        return activity

