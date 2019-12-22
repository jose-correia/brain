import logging
import os
from flask import current_app
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.services.files.find_image_service import FindImageService


logger = logging.getLogger(__name__)


class UploadImageService(object):
    def __init__(self, file, name, folder):
        self.file = file
        self.name = name
        self.folder = folder

    def call(self):
        if self.file.filename == '':
            return False, 'No file selected for uploading'

        if self.file and self.__allowed_image(self.file.filename):
            extension = self.__get_extension(self.file.filename)
            filename = self.name.lower().replace(' ', '_') + '.' + extension
            try:
                self.file.save(os.path.join(current_app.root_path, self.folder, filename))

                # erases other existing images with different extensions
                for allowed_extension in current_app.config['ALLOWED_IMAGES']:
                    if allowed_extension != extension:
                        filename = self.name.lower().replace(' ', '_') + '.' + allowed_extension
                        DeleteImageService(filename, self.folder).call()

                return True, None

            except Exception as e:
                logger.error(e)
                return False, 'Image upload failed'
        return False, 'File extension is not allowed'

    def __allowed_image(self, filename):
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_IMAGES']
    
    def __get_extension(self, filename): 
        return filename.rsplit('.', 1)[1].lower()

            
