import logging
from jeec_brain.models.meals import Meals
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateMealService:
    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Meals]:

        meal = Meals.create(**self.kwargs)

        if not meal:
            return None

        return meal
