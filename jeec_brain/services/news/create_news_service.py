import logging
from jeec_brain.models.news import News
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateNewsService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[News]:
        
        news = News.create(**self.kwargs)

        if not news:
            return None

        return news

