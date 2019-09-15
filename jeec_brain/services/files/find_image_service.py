import os
from flask import current_app


class FindImageService(object):
    def __init__(self, name, folder):
        self.name = name
        self.folder = folder

    def call(self):
        for extension in current_app.config['ALLOWED_IMAGES']:
            image_filename = self.name.lower().replace(' ', '_') + '.' + extension

            if os.path.isfile(os.path.join(current_app.root_path, self.folder, image_filename)): 
                return f'/{self.folder}/{image_filename}'
            
        return None
