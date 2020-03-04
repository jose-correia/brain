from jeec_brain.models.news import News


class NewsFinder():

    @classmethod
    def get_news_from_external_id(cls, external_id):
        return News.query().filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all_news(cls):
        return News.query().order_by(News.updated_at).all()

    @classmethod
    def get_news_from_day(cls, day):
        return News.query().filter(News.day.ilike(day)).order_by(News.updated_at).all()

    @classmethod
    def get_news_from_parameters(cls, kwargs):
        try:
            return News.query().filter_by(**kwargs).all()
        except Exception:
            return None
    