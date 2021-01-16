from jeec_brain.apps.companies_api import bp
from flask import render_template, session, request, redirect, url_for
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.finders.meals_finder import MealsFinder
from jeec_brain.handlers.meals_handler import MealsHandler
from jeec_brain.services.meals.get_dish_types_service import GetDishTypesService
from jeec_brain.values.api_error_value import APIErrorValue
from datetime import datetime
import json

@bp.route('/meals', methods=['GET'])
@require_company_login
def meals_dashboard(company_user):
    meals_list = company_user.company.meals

    open_registrations = []

    if meals_list is None or len(meals_list) == 0:
        error = 'No meals found'
        return render_template('companies/meals/meals_dashboard.html', meals=None, open_registrations=None, error=error, company=company_user.company)

    for meal in meals_list:
        try:
            registration_time = datetime.strptime(meal.registration_day + ' ' + meal.registration_time, '%d %m %Y, %a %H:%M')

            if registration_time < datetime.now():
                open_registrations.append(False)
            else:
                open_registrations.append(True)
        except:
            open_registrations.append(False)

    return render_template('companies/meals/meals_dashboard.html', meals=meals_list, open_registrations=open_registrations, error=None, company=company_user.company)


@bp.route('/meal/<string:meal_external_id>', methods=['GET'])
@require_company_login
def get_meal(company_user, meal_external_id):
    # get meal
    meal = MealsFinder.get_meal_from_external_id(meal_external_id)

    if meal is None:
        return APIErrorValue('Couldnt find meal').json(400)

    # check if company is allowed in meal
    if company_user.company not in MealsFinder.get_companies_from_meal_id(meal.id):
        return APIErrorValue('Company not allowed in this meal').json(400)

    # get company meal
    company_meal = MealsFinder.get_company_meals_from_meal_id_and_company_id(meal.id, company_user.company_id)

    if company_meal is None:
        return APIErrorValue('Couldnt find company meal').json(400)

    # get dishes from meal
    dishes = MealsFinder.get_dishes_from_meal_id(meal_external_id)

    # get company dishes
    company_dishes = MealsFinder.get_company_dishes_from_meal_id_and_company_id(meal.id, company_user.company_id)

    dish_types = []
    for dish in dishes:
        if(dish.type.name not in dish_types):
            dish_types.append(dish.type.name)

    if dishes is None:
        return render_template('companies/meals/meal.html', \
            meal=meal, \
            max_dish_quantity=None, \
            dish_types=None, \
            dishes=None, \
            company_dishes=None, \
            error='No dishes found.', \
            user=company_user)

    return render_template('companies/meals/meal.html', \
        meal=meal, \
        max_dish_quantity=company_meal.max_dish_quantity, \
        dish_types=dish_types, \
        dishes=dishes, \
        company_dishes=company_dishes, \
        error=None, \
        user=company_user)


@bp.route('/meal/<string:meal_external_id>', methods=['POST'])
@require_company_login
def choose_dishes(company_user, meal_external_id):
    # get meal
    meal = MealsFinder.get_meal_from_external_id(meal_external_id)
    
    try:
        registration_time = datetime.strptime(meal.registration_day + ' ' + meal.registration_time, '%d %m %Y, %a %H:%M')

        # check if date past registration date
        if registration_time < datetime.now():
            return APIErrorValue('Past registration time. Cant choose meal.').json(400)
    except:
        return APIErrorValue('Past registration time. Cant choose meal.').json(400)
        
    # eliminate previous company dishes
    company_dishes = MealsFinder.get_company_dishes_from_meal_id_and_company_id(meal.id, company_user.company_id)

    if company_dishes:
        for company_dish in company_dishes:
            MealsHandler.delete_company_dish(company_dish)

    # get company meal
    company_meal = MealsFinder.get_company_meals_from_meal_id_and_company_id(meal.id, company_user.company_id)

    if company_meal is None:
        return APIErrorValue('Couldnt find company meal').json(400)

    # get dishes
    dish_ids = []
    dish_quantities = []
    
    for dish_type in GetDishTypesService.call():
        dish_ids_by_type = request.form.getlist('dish_'+dish_type)
        dish_quantities_by_type = request.form.getlist('dish_quantity_'+dish_type)

        if dish_ids_by_type is None or dish_quantities_by_type is None:
            continue
        
        if company_meal.max_dish_quantity is not None:
            try:
                if sum(list(map(int, filter(None, dish_quantities_by_type)))) > company_meal.max_dish_quantity:
                    return APIErrorValue('Number of ' + dish_type + 's over maximum value!').json(500)
            except Exception as e:
                return APIErrorValue('Quantities type not int, '+str(e)).json(500)
            
            for dish_quantity_by_type in dish_quantities_by_type:
                if dish_quantity_by_type is not None and not isinstance(dish_quantity_by_type,int):
                    return APIErrorValue('Quantities type not int').json(500)

        dish_ids += dish_ids_by_type
        dish_quantities += dish_quantities_by_type


    if dish_ids:
        for index, dish_id in enumerate(dish_ids):
            dish = MealsFinder.get_dishes_from_dish_external_id(dish_id)

            if dish is None:
                return APIErrorValue('Couldnt find dish').json(500)

            try:
                dish_quantity = int(dish_quantities[index])
            except ValueError:
                continue
            except TypeError:
                continue
            except IndexError:
                return APIErrorValue('Quantities size different from dishes').json(500)

            MealsHandler.add_company_dish(
                company=company_user.company,
                dish=dish,
                dish_quantity=dish_quantity
            )

    return redirect(url_for('companies_api.meals_dashboard'))

