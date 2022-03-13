from jeec_brain.models.dishes import Dishes


class DeleteDishService:
    def __init__(self, dish: Dishes):
        self.dish = dish

    def call(self) -> bool:
        result = self.dish.delete()
        return result
