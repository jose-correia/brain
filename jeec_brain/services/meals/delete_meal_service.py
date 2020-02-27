from jeec_brain.models.meals import Meals


class DeleteMealService():

    def __init__(self, meal: Meals):
        self.meal = meal

    def call(self) -> bool:
        result = self.meal.delete()
        return result
