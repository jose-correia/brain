from config import Config
from jwt import decode

import logging
logger = logging.getLogger(__name__)

class DecodeJwtService(object):

    @classmethod
    def __init__(self, token):
        self.token = token
        self.secret = Config.SECRET_KEY

    def call(self):
        try:
            if self.token is None:
                return None
                
            return decode(self.token, self.secret, algorithm='HS256') 
        except Exception as e:
            logger.error(e)


        