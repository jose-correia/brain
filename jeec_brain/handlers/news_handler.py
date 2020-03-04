from flask import current_app
# SERVICES
from jeec_brain.services.news.create_news_service import CreateNewsService
from jeec_brain.services.news.delete_news_service import DeleteNewsService
from jeec_brain.services.news.update_news_service import UpdateNewsService
from jeec_brain.services.files.upload_image_service import UploadImageService
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.services.files.find_image_service import FindImageService


class NewsHandler():

    @classmethod
    def create_news(cls, **kwargs):
        return CreateNewsService(kwargs=kwargs).call()

    @classmethod
    def delete_news(cls, news):
        news_id = news.external_id

        if DeleteNewsService(news).call():
            for extension in current_app.config['ALLOWED_IMAGES']:
                filename = f'{news_id}.{extension}'
                DeleteImageService(filename, 'static/events/images').call()
            
            return DeleteNewsService(news)
        return False

    @classmethod
    def update_news(cls, news, **kwargs):
        return UpdateNewsService(news, kwargs).call()

    @classmethod
    def upload_image(cls, file, image_name):
        return UploadImageService(file, image_name, 'static/news/images').call()

    @classmethod
    def find_image(cls, image_name):
        return FindImageService(image_name, 'static/news/images').call()

