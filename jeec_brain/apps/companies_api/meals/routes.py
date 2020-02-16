from jeec_brain.apps.companies_api import bp
from flask import render_template, session, request, redirect, url_for
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.finders.meals_finder import MealsFinder
from jeec_brain.handlers.meals_handler import MealsHandler
from jeec_brain.values.api_error_value import APIErrorValue
from datetime import datetime


@bp.route('/meals', methods=['GET'])
@require_company_login
def meals_dashboard():
    if current_user.company is None:
        return APIErrorValue('Couldnt find company').json(400)

    meals_list = current_user.company.meals

    if meals_list is None or len(meals_list) == 0:
        error = 'No meals found'
        return render_template('admin/meals/meals_dashboard.html', meals=None, error=error, company=current_user.company)

    return render_template('companies/meals/meals_dashboard.html', meals=meals_list, error=None, company=current_user.company)


@bp.route('/meal/<string:meal_external_id>', methods=['GET'])
@require_company_login
def get_meal(meal_external_id):
    if current_user.company is None:
        return APIErrorValue('Couldnt find company').json(400)

    # get meal
    meal = MealsFinder.get_meal_from_external_id(meal_external_id)

    if meal is None:
        return APIErrorValue('Couldnt find meal').json(400)

    # get dishes from meal
    dishes = MealsFinder.get_dishes_from_meal_id(meal_external_id)

    # check if company is allowed in meal
    if current_user.company not in MealsFinder.get_companies_from_meal_id(meal.id):
        return APIErrorValue('Company not allowed in this meal').json(400)

    return render_template('companies/meals/meal.html', \
        meal=meal, \
        dishes=dishes,
        error=None, \
        user=current_user)


@bp.route('/meal/<string:meal_external_id>', methods=['POST'])
@require_company_login
def choose_dishes(meal_external_id):
    if current_user.company is None:
        return APIErrorValue('Couldnt find company').json(400)
    
    # get meal
    meal = MealsFinder.get_meal_from_external_id(meal_external_id)
    registration_time = datetime.strptime(meal.registration_day + meal.registration_time, '%b %d %Y %I:%M%p')

    # check if date past registration date
    if registration_time > datetime.now():
        return APIErrorValue('Past registration time. Cant choose meal.').json(400)

    # eliminate previous company dishes
    company_dishes = MealsFinder.get_company_dishes_from_meal_id_and_company_id(meal_external_id, current_user.company_id)

    if company_dishes:
        for company_dish in company_dishes:
            MealsHandler.delete_company_dish(company_dish)

    # get dishes
    dishes = request.form.getlist('dish')

    if dishes:
        for dish in dishes:
            if dish is None:
                return APIErrorValue('Couldnt find dish').json(500)

            MealsHandler.add_company_dish(
                company=current_user.company,
                dish=dish
            )

    return redirect(url_for('companies_api.meals_dashboard'))

