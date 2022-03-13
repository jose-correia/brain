import logging
from jeec_brain.models.dishes import Dishes
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateDishService:
    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Dishes]:

        dish = Dishes.create(**self.kwargs)

        if not dish:
            return None

        return dish
