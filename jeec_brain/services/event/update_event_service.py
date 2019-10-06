from typing import Dict, Optional
from jeec_brain.models.event import Event


class UpdateEventService():
    
    def __init__(self, event: Event, kwargs: Dict):
        self.event = event
        self.kwargs = kwargs

    def call(self) -> Optional[Event]:
        update_result = self.event.update(**self.kwargs)
        return update_result
