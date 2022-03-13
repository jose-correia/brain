from typing import Dict, Optional
from jeec_brain.models.events import Events


class UpdateEventService:
    def __init__(self, event: Events, kwargs: Dict):
        self.event = event
        self.kwargs = kwargs

    def call(self) -> Optional[Events]:
        update_result = self.event.update(**self.kwargs)
        return update_result
