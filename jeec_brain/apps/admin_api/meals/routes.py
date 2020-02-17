from .. import bp
from flask import render_template, current_app, request, redirect, url_for
from jeec_brain.finders.meals_finder import MealsFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.handlers.meals_handler import MealsHandler
from jeec_brain.services.meals.get_meal_types_service import GetMealTypesService
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
from jeec_brain.models.enums.meal_type_enum import MealTypeEnum
from flask_login import current_user


# Meals routes
@bp.route('/meals', methods=['GET'])
@allow_all_roles
def meals_dashboard():
    meal_types = GetMealTypesService.call()
    search_parameters = request.args
    day = request.args.get('day')

    # handle search bar requests
    if day is not None:
        search = day
        meals_list = MealsFinder.get_meals_from_day(day)

    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = 'search by day'

        meals_list = MealsFinder.get_meals_from_parameters(search_parameters)

    # request endpoint with no parameters should return all meals
    else:
        search = None
        meals_list = MealsFinder.get_all_meals()

    if meals_list is None or len(meals_list) == 0:
        error = 'No results found'
        return render_template('admin/meals/meals_dashboard.html', meals=None, meal_types=meal_types, error=error, search=search, role=current_user.role.name)

    return render_template('admin/meals/meals_dashboard.html', meals=meals_list, meal_types=meal_types, error=None, search=search, role=current_user.role.name)


@bp.route('/new-meal', methods=['GET'])
@allowed_roles(['admin', 'companies_admin'])
def add_meal_dashboard():
    companies = CompaniesFinder.get_all()
    meal_types = GetMealTypesService.call()
    return render_template('admin/meals/add_meal.html', \
        meal_types = meal_types, \
        companies=companies, \
        error=None)


@bp.route('/new-meal', methods=['POST'])
@allowed_roles(['admin', 'companies_admin'])
def create_meal():
    # extract form parameters
    meal_type = request.form.get('type')
    location = request.form.get('location')
    day = request.form.get('day')
    time = request.form.get('time')
    registration_day = request.form.get('day')
    registration_time = request.form.get('time')

    if meal_type not in GetMealTypesService.call():
        return 'Wrong meal type provided', 404
    else:
        meal_type = MealTypeEnum[meal_type]

    # create new meal
    meal = MealsHandler.create_meal(
            type=meal_type,
            location=location,
            day=day,
            time=time,
            registration_day=registration_day,
            registration_time=registration_time
        )

    if meal is None:
        return render_template('admin/meals/add_meal.html', \
            type=meal_type, \
            companies=CompaniesFinder.get_all(), \
            error="Failed to create meal!")

    # extract company names and max dish quantities from parameters
    companies = request.form.getlist('company')
    max_dish_quantities = request.form.getlist('max_dish_quantity')

    # if company names where provided
    if companies:
        for index, name in enumerate(companies):
            company = CompaniesFinder.get_from_name(name)
            if company is None:
                return APIErrorValue('Couldnt find company').json(500)

            try:
                max_dish_quantity = max_dish_quantities[index]
            except:
                pass

            company_meal = MealsHandler.add_company_meal(company, meal, max_dish_quantity)
            if company_meal is None:
                return APIErrorValue('Failed to create company meal').json(500)
    
    # extract dish names and descriptions from parameters
    dish_names = request.form.getlist('dish_name')
    dish_descriptions = request.form.getlist('dish_description')

    # if dishes names where provided
    if dish_names:
        for index, name in enumerate(dish_names):
            if not name:
                continue

            try:
                dish_description = dish_descriptions[index]
            except:
                pass

            meal_dish = MealsHandler.create_dish(
                name = name,
                description = dish_description,
                meal_id = meal.id
            )
            if meal_dish is None:
                return APIErrorValue('Failed to create dish').json(500)

    return redirect(url_for('admin_api.meals_dashboard'))


@bp.route('/meal/<string:meal_external_id>', methods=['GET'])
@allowed_roles(['admin', 'companies_admin'])
def get_meal(meal_external_id):
    meal = MealsFinder.get_meal_from_external_id(meal_external_id)
    companies = CompaniesFinder.get_all()
    meal_types = GetMealTypesService.call()
    company_meals = MealsFinder.get_company_meals_from_meal_id(meal_external_id)
    dishes = MealsFinder.get_dishes_from_meal_id(meal_external_id)

    return render_template('admin/meals/update_meal.html', \
        meal=meal, \
        meal_types=meal_types, \
        companies=companies, \
        company_meals=[company.company_id for company in company_meals], \
        dishes=dishes, \
        error=None)

@bp.route('/meal/<string:meal_external_id>', methods=['POST'])
@allowed_roles(['admin', 'companies_admin'])
def update_meal(meal_external_id):
    meal = MealsFinder.get_meal_from_external_id(meal_external_id)
    company_meals = MealsFinder.get_company_meals_from_meal_id(meal_external_id)
    dishes = MealsFinder.get_dishes_from_meal_id(meal_external_id)

    if meal is None:
        return APIErrorValue('Couldnt find meal').json(500)

    # extract form parameters
    meal_type = request.form.get('type')
    location = request.form.get('location')
    day = request.form.get('day')
    time = request.form.get('time')
    registration_day = request.form.get('day')
    registration_time = request.form.get('time')

    if meal_type not in GetMealTypesService.call():
        return 'Wrong meal type provided', 404
    else:
        meal_type = MealTypeEnum[meal_type]

    updated_meal = MealsHandler.update_meal(
        meal=meal,
        type=meal_type,
        location=location,
        day=day,
        time=time,
        registration_day=registration_day,
        registration_time=registration_time
    )

    if company_meals:
        for company_meal in company_meals:
            MealsHandler.delete_company_meal(company_meal)

    if dishes:
        for dish in dishes:
            MealsHandler.delete_dish(dish)

    # extract company names and max dish quantities from parameters
    companies = request.form.getlist('company')
    max_dish_quantities = request.form.getlist('max_dish_quantity')

    # if company names where provided
    if companies:
        for index, name in enumerate(companies):
            company = CompaniesFinder.get_from_name(name)
            if company is None:
                return APIErrorValue('Couldnt find company').json(500)

            try:
                max_dish_quantity = max_dish_quantities[index]
            except:
                max_dish_quantity = 2

            company_meal = MealsHandler.add_company_meal(company, meal, max_dish_quantity)
            if company_meal is None:
                return APIErrorValue('Failed to create company meal').json(500)
    
    # extract dish names and descriptions from parameters
    dish_names = request.form.getlist('dish_name')
    dish_descriptions = request.form.getlist('dish_description')

    # if dishes names where provided
    if dish_names:
        for index, name in enumerate(dish_names):
            if not name:
                continue
            
            try:
                dish_description = dish_descriptions[index]
            except:
                pass

            meal_dish = MealsHandler.create_dish(
                name = name,
                description = dish_description,
                meal_id = meal.id
            )
            if meal_dish is None:
                return APIErrorValue('Failed to create dish').json(500)
                
    if updated_meal is None:
        return render_template('admin/meals/update_meal.html', \
            meal=meal, \
            types=GetMealTypesService.call(), \
            companies=CompaniesFinder.get_all(), \
            error="Failed to update meal!")

    return redirect(url_for('admin_api.meals_dashboard'))


@bp.route('/meal/<string:meal_external_id>/delete', methods=['GET'])
@allowed_roles(['admin', 'companies_admin'])
def delete_meal(meal_external_id):
    meal = MealsFinder.get_meal_from_external_id(meal_external_id)
    company_meals = MealsFinder.get_company_meals_from_meal_id(meal_external_id)
    dishes = MealsFinder.get_dishes_from_meal_id(meal_external_id)

    if meal is None:
        return APIErrorValue('Couldnt find meal').json(500)
        
    if company_meals:
        for company_meal in company_meals:
            MealsHandler.delete_company_meal(company_meal)

    if dishes:
        for dish in dishes:
            MealsHandler.delete_dish(dish)

    if MealsHandler.delete_meal(meal):
        return redirect(url_for('admin_api.meals_dashboard'))

    else:
        return render_template('admin/meals/update_meal.html', meal=meal, error="Failed to delete meal!")


@bp.route('/meal/<string:meal_external_id>/dishes', methods=['GET'])
@allowed_roles(['admin', 'companies_admin'])
def meal_dishes(meal_external_id):
    meal = MealsFinder.get_meal_from_external_id(meal_external_id)

    if meal is None:
        return APIErrorValue('Couldnt find meal').json(500)

    company_meals = MealsFinder.get_company_meals_from_meal_id(meal_external_id)
    dishes = MealsFinder.get_dishes_from_meal_id(meal_external_id)
    company_dishes = MealsFinder.get_company_dishes_from_meal_id(meal.id)

    return render_template('admin/meals/meal_dishes.html', \
        meal=meal, \
        companies=companies, \
        company_meals=[company.company_id for company in company_meals], \
        dishes=dishes, \
        error=None)