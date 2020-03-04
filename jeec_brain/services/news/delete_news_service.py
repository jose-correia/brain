from jeec_brain.models.news import News


class DeleteNewsService():

    def __init__(self, news: News):
        self.news = news

    def call(self) -> bool:
        result = self.news.delete()
        return result
