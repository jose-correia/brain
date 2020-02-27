from jeec_brain.models.enums.meal_type_enum import MealTypeEnum


class GetMealTypesService():

    def call():
        return dir(MealTypeEnum)[0:4]
