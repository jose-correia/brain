from jeec_brain.models.colaborators import Colaborators


class DeleteColaboratorService():

    def __init__(self, colaborator: Colaborators):
        self.colaborator = colaborator

    def call(self) -> bool:
        result = self.colaborator.delete()
        return result
