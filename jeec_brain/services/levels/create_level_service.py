from jeec_brain.models.levels import Levels

class CreateLevelService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self):        
        level = Levels.create(**self.kwargs)

        if not level:
            return None

        return level