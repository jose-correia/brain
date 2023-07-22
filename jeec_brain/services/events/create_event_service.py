import logging
from jeec_brain.models.events import Events
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateEventService:
    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Events]:

        event = Events.create(**self.kwargs)

        if not event:
            return None

        return event
