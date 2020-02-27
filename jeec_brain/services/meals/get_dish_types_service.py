from jeec_brain.models.enums.dish_type_enum import DishTypeEnum


class GetDishTypesService():

    def call():
        return dir(DishTypeEnum)[0:4]
