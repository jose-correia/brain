import logging
from jeec_brain.models.tags import Tags
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateTagService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Tags]:
        
        tag = Tags.create(**self.kwargs)

        if not tag:
            return None

        return tag

