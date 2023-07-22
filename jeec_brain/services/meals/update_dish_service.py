from typing import Dict, Optional
from jeec_brain.models.dishes import Dishes


class UpdateDishService:
    def __init__(self, dish: Dishes, kwargs: Dict):
        self.dish = dish
        self.kwargs = kwargs

    def call(self) -> Optional[Dishes]:
        update_result = self.dish.update(**self.kwargs)
        return update_result
