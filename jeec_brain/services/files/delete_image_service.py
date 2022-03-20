import logging
import os
from flask import current_app

logger = logging.getLogger(__name__)


class DeleteImageService(object):
    def __init__(self, filename, folder):
        self.filename = filename
        self.folder = folder

    def call(self):
        try:
            os.remove(os.path.join(current_app.root_path, self.folder, self.filename))
            return True
        except Exception as e:
            logger.error(e)
            pass

        return False
