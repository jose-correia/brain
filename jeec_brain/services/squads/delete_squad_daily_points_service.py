from jeec_brain.models.squads_daily_points import SquadDailyPoints


class DeleteSquadDailyPointsService():

    def __init__(self, squad_daily_points: SquadDailyPoints):
        self.squad_daily_points = squad_daily_points

    def call(self) -> bool:
        result = self.squad_daily_points.delete()
        return result
