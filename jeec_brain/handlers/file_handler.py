import os
from flask import current_app
from config import Config
from jeec_brain.services.files.compress_files_service import CompressFilesService

import logging
logger = logging.getLogger(__name__)


class FileHandler(object):

    @staticmethod
    def get_files_zip():
        try:
            zip_file = CompressFilesService().call()
            return zip_file
        except Exception as e:
            logger.error(e)
            return None

    @staticmethod
    def upload_file(file, filename):
        try:
            file.save(os.path.join(current_app.root_path, 'storage', filename))
            return True
        except Exception as e:
            logger.error(e)
            return False

    @staticmethod
    def delete_file(filename):
        try:
            os.remove(os.path.join(current_app.root_path, 'storage', filename))
        except Exception as e:
            logger.error(e)
            return False

    @staticmethod
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

