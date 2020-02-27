from typing import Dict, Optional
from jeec_brain.models.meals import Meals


class UpdateMealService():
    
    def __init__(self, meal: Meals, kwargs: Dict):
        self.meal = meal
        self.kwargs = kwargs

    def call(self) -> Optional[Meals]:
        update_result = self.meal.update(**self.kwargs)
        return update_result
