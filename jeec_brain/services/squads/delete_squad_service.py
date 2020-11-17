from jeec_brain.models.squads import Squads


class DeleteSquadService():

    def __init__(self, squad: Squads):
        self.squad = squad

    def call(self) -> bool:
        result = self.squad.delete()
        return result
