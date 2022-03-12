import os
from flask import current_app


class RenameImageService(object):
    def __init__(self, folder, old_name, new_name):
        self.folder = folder
        self.old_name = old_name
        self.new_name = new_name

    def call(self):
        for extension in current_app.config["ALLOWED_IMAGES"]:
            old_image_filename = (
                self.old_name.lower().replace(" ", "_") + "." + extension
            )
            old_file = os.path.join(
                current_app.root_path, self.folder, old_image_filename
            )

            new_image_filename = (
                self.new_name.lower().replace(" ", "_") + "." + extension
            )
            new_file = os.path.join(
                current_app.root_path, self.folder, new_image_filename
            )

            if os.path.isfile(old_file):
                os.rename(old_file, new_file)

            return True
        return False
