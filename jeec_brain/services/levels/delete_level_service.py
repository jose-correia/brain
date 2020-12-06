from jeec_brain.models.levels import Levels


class DeleteLevelService():

    def __init__(self, level: Levels):
        self.level = level

    def call(self) -> bool:
        result = self.level.delete()
        return result