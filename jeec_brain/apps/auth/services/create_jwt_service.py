from config import Config
from jwt import encode

import logging
logger = logging.getLogger(__name__)

class CreateJwtService(object):

    @classmethod
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.secret = Config.SECRET_KEY

    def call(self):
        try:
            return encode({'username': self.username, 'email': self.email}, self.secret, algorithm='HS256')
        except Exception as e:
            logger.error(e)


        