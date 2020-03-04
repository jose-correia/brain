from typing import Dict, Optional
from jeec_brain.models.news import News


class UpdateNewsService():
    
    def __init__(self, news: News, kwargs: Dict):
        self.news = news
        self.kwargs = kwargs

    def call(self) -> Optional[News]:
        update_result = self.news.update(**self.kwargs)
        return update_result
