from jeec_brain.apps.companies_api import bp
from flask import render_template, session, request, redirect, url_for, jsonify, make_response
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.finders.meals_finder import MealsFinder
from jeec_brain.handlers.meals_handler import MealsHandler
from jeec_brain.services.meals.get_dish_types_service import GetDishTypesService
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.companies_api.meals.schemas import *
from datetime import datetime
import json
from jeec_brain.apps.auth.wrappers import requires_client_auth


@bp.get("/meals")
#@require_company_login
def meals_dashboard(company_user):
    meals_list = company_user.company.meals

    open_registrations = []

    if meals_list is None or len(meals_list) == 0:
        error = "No meals found"
        return render_template(
            "companies/meals/meals_dashboard.html",
            meals=None,
            open_registrations=None,
            error=error,
            company=company_user.company,
        )

    for meal in meals_list:
        try:
            registration_time = datetime.strptime(
                meal.registration_day + " " + meal.registration_time,
                "%d %m %Y, %A %H:%M",
            )

            if registration_time < datetime.now():
                open_registrations.append(False)
            else:
                open_registrations.append(True)
        except:
            open_registrations.append(False)

    return render_template(
        "companies/meals/meals_dashboard.html",
        meals=meals_list,
        open_registrations=open_registrations,
        error=None,
        company=company_user.company,
    )


@bp.get("/meal/<string:meal_external_id>")
#@require_company_login
def get_meal(company_user, path: MealPath):
    # get meal
    meal = MealsFinder.get_meal_from_external_id(path.meal_external_id)

    if meal is None:
        return APIErrorValue("Couldnt find meal").json(400)

    # check if company is allowed in meal
    if company_user.company not in MealsFinder.get_companies_from_meal_id(meal.id):
        return APIErrorValue("Company not allowed in this meal").json(400)

    # get company meal
    company_meal = MealsFinder.get_company_meals_from_meal_id_and_company_id(
        meal.id, company_user.company_id
    )

    if company_meal is None:
        return APIErrorValue("Couldnt find company meal").json(400)

    # get dishes from meal
    dishes = MealsFinder.get_dishes_from_meal_id(path.meal_external_id)

    # get company dishes
    company_dishes = MealsFinder.get_company_dishes_from_meal_id_and_company_id(
        meal.id, company_user.company_id
    )

    dish_types = []
    for dish in dishes:
        if dish.type.name not in dish_types:
            dish_types.append(dish.type.name)

    if dishes is None:
        return render_template(
            "companies/meals/meal.html",
            meal=meal,
            max_dish_quantity=None,
            dish_types=None,
            dishes=None,
            company_dishes=None,
            error="No dishes found.",
            user=company_user,
        )

    return render_template(
        "companies/meals/meal.html",
        meal=meal,
        max_dish_quantity=company_meal.max_dish_quantity,
        dish_types=dish_types,
        dishes=dishes,
        company_dishes=company_dishes,
        error=None,
        user=company_user,
    )


@bp.post("/meal/<string:meal_external_id>")
#@require_company_login
def choose_dishes(company_user, path: MealPath):
    # get meal
    meal = MealsFinder.get_meal_from_external_id(path.meal_external_id)

    try:
        registration_time = datetime.strptime(
            meal.registration_day + " " + meal.registration_time, "%d %m %Y, %A %H:%M"
        )

        # check if date past registration date
        if registration_time < datetime.now():
            return APIErrorValue("Past registration time. Cant choose meal.").json(400)
    except:
        return APIErrorValue("Past registration time. Cant choose meal.").json(400)

    # eliminate previous company dishes
    company_dishes = MealsFinder.get_company_dishes_from_meal_id_and_company_id(
        meal.id, company_user.company_id
    )

    if company_dishes:
        for company_dish in company_dishes:
            MealsHandler.delete_company_dish(company_dish)

    # get company meal
    company_meal = MealsFinder.get_company_meals_from_meal_id_and_company_id(
        meal.id, company_user.company_id
    )

    if company_meal is None:
        return APIErrorValue("Couldnt find company meal").json(400)

    # get dishes
    dish_ids = []
    dish_quantities = []

    for dish_type in GetDishTypesService.call():
        dish_ids_by_type = request.form.getlist("dish_" + dish_type)
        dish_quantities_by_type = request.form.getlist("dish_quantity_" + dish_type)

        if dish_ids_by_type is None or dish_quantities_by_type is None:
            continue

        if company_meal.max_dish_quantity is not None:
            try:
                if (
                    sum(list(map(int, filter(None, dish_quantities_by_type))))
                    > company_meal.max_dish_quantity
                ):
                    return APIErrorValue(
                        "Number of " + dish_type + "s over maximum value!"
                    ).json(500)
            except Exception as e:
                return APIErrorValue("Quantities type not int, " + str(e)).json(500)

            for dish_quantity_by_type in dish_quantities_by_type:
                if dish_quantity_by_type is not None and not isinstance(
                    dish_quantity_by_type, int
                ):
                    return APIErrorValue("Quantities type not int").json(500)

        dish_ids += dish_ids_by_type
        dish_quantities += dish_quantities_by_type

    if dish_ids:
        for index, dish_id in enumerate(dish_ids):
            dish = MealsFinder.get_dishes_from_dish_external_id(dish_id)

            if dish is None:
                return APIErrorValue("Couldnt find dish").json(500)

            try:
                dish_quantity = int(dish_quantities[index])
            except ValueError:
                continue
            except TypeError:
                continue
            except IndexError:
                return APIErrorValue("Quantities size different from dishes").json(500)

            MealsHandler.add_company_dish(
                company=company_user.company, dish=dish, dish_quantity=dish_quantity
            )

    return redirect(url_for("companies_api.meals_dashboard"))

@bp.post("/mealsdashboard")
#@requires_client_auth
def meals_dashboard_vue():
    company_name = json.loads(request.data.decode('utf-8'))['company']

    company = CompaniesFinder.get_from_name(company_name)
    meals_list = company.meals

    if meals_list is None or len(meals_list) == 0:
        error = "No meals found"
        return make_response(
        jsonify({
            "meals":None,"error":error,"length":0
        })
        )

    json_meals=[]
    for meal in meals_list:
        open_registrations = False
        try:
            registration_time = datetime.strptime(
                meal.registration_day + " " + meal.registration_time,
                "%d %m %Y, %A %H:%M",
            )
            # print(registration_time)
            if registration_time < datetime.now():
                open_registrations = False
            else:
                open_registrations = True
        except:
            open_registrations = False
        
        json_meal = {
            "open_registrations":open_registrations,
            "name":meal.type.name,
            "day":meal.day,
            "time":meal.time,
            "location":meal.location,
            "external_id":meal.external_id
        }
        json_meals.append(json_meal)

        # print(json_meal)

    return make_response(
        jsonify({
            "meals":json_meals,"error":"","length":len(json_meals)
        })
        )

@bp.post("/mealsdashboard/meal")
#@requires_client_auth
def get_meal_vue():
    meal_external_id = json.loads(request.data.decode('utf-8'))['meal_external_id']

    if(len(meal_external_id)!=36):
        return make_response(
        jsonify({
            "meal":{
                "type":"",
                "day":"",
            },"error":"Non valid id",
            "max_dish_quantity":3,
            "dish_types":None,
            "dishes":None,
        })
        )
    # get meal
    meal = MealsFinder.get_meal_from_external_id(meal_external_id)

    company_name = json.loads(request.data.decode('utf-8'))['company']

    company = CompaniesFinder.get_from_name(company_name)



    if meal is None:
        return make_response(
        jsonify({
            "meal":{
                "type":"",
                "day":"",
            },"error":"Couldn't find meal",
            "max_dish_quantity":None,
            "dish_types":None,
            "dishes":None,
        })
        )

    # check if company is allowed in meal
    if company not in MealsFinder.get_companies_from_meal_id(meal.id):
        return make_response(
        jsonify({
            "meal":{
                "type":"",
                "day":"",
            },"error":"Company not allowed in this meal",
            "max_dish_quantity":None,
            "dish_types":None,
            "dishes":None,
        })
        )

    # get company meal
    company_meal = MealsFinder.get_company_meals_from_meal_id_and_company_id(
        meal.id, company.id
    )

    if company_meal is None:
        return make_response(
        jsonify({
            "meal":{
                "type":"",
                "day":"",
            },"error":"Couldn't find company meal",
            "max_dish_quantity":None,
            "dish_types":None,
            "dishes":None,
        })
        )

    # get dishes from meal
    dishes = MealsFinder.get_dishes_from_meal_id(meal_external_id)
    json_dishes=[]

    # get company dishes
    company_dishes = MealsFinder.get_company_dishes_from_meal_id_and_company_id(
        meal.id, company.id
    )
    for dish in dishes:
        quantity=0,
        for company_dish in company_dishes:
            if company_dish.dish_id == dish.id:
                quantity = company_dish.dish_quantity
        json_dish={
            "type":dish.type.name,
            "name":dish.name,
            "description":dish.description,
            "external_id":dish.external_id,
            "quantity":quantity
        }
        json_dishes.append(json_dish)

    dish_types = []
    for dish in dishes:
        if dish.type.name not in dish_types:
            dish_types.append(dish.type.name)

    if dishes is None:
        return make_response(
        jsonify({
            "meal":{
                "type":meal.type.name,
                "day":meal.day
            },"error":"No dishes found",
            "max_dish_quantity":None,
            "dish_types":None,
            "dishes":None,
        })
        )
    
    return make_response(
        jsonify({
            "meal":{
                "type":meal.type.name,
                "day":meal.day
            },"error":"",
            "max_dish_quantity":company_meal.max_dish_quantity,
            "dish_types":dish_types,
            "dishes":json_dishes,
        })
        )

@bp.post("mealsdashboard/meal/change")
@requires_client_auth
def change_dishes():
    meal_external_id = json.loads(request.data.decode('utf-8'))['meal_external_id']
    # get meal
    meal = MealsFinder.get_meal_from_external_id(meal_external_id)

    company_name = json.loads(request.data.decode('utf-8'))['company']

    company = CompaniesFinder.get_from_name(company_name)

    try:
        registration_time = datetime.strptime(
            meal.registration_day + " " + meal.registration_time, "%d %m %Y, %A %H:%M"
        )

        # check if date past registration date
        if registration_time < datetime.now():
            return APIErrorValue("Past registration time. Cant choose meal.").json(400)
    except:
        return APIErrorValue("Past registration time. Cant choose meal.").json(400)

    # eliminate previous company dishes
    company_dishes = MealsFinder.get_company_dishes_from_meal_id_and_company_id(
        meal.id, company.id
    )

    if company_dishes:
        for company_dish in company_dishes:
            MealsHandler.delete_company_dish(company_dish)

    # get company meal
    company_meal = MealsFinder.get_company_meals_from_meal_id_and_company_id(
        meal.id, company.id
    )

    if company_meal is None:
        return APIErrorValue("Couldnt find company meal").json(400)

    # get dishes
    # print(json.loads(request.data.decode('utf-8')))
    form_dishes = json.loads(request.data.decode('utf-8'))['dishes']
    dish_quantity = 0
    for dish in form_dishes:
        if dish['quantity'] != [0]:
            quantity_dish = int(dish['quantity'])
        else:
            quantity_dish = 0
        dish_quantity += quantity_dish
    
    if(dish_quantity > 3):
        return APIErrorValue("You can only add three meals total").json(200)
    
    quantity_dish = 0
    for dish_type in GetDishTypesService.call():
        quantity=0
        for dish in form_dishes:
            if(dish['type']==dish_type):
                if dish['quantity'] != [0]:
                    quantity_dish = int(dish['quantity'])
                else:
                    quantity_dish = 0
                quantity+=quantity_dish
               
        if(company_meal.max_dish_quantity is not None and quantity>company_meal.max_dish_quantity):
            return APIErrorValue(
                    "Number of " + dish_type + "s over maximum value!"
                ).json(500)
    for form_dish in form_dishes:
        dish = MealsFinder.get_dishes_from_dish_external_id(form_dish['external_id'])
        if dish is None:
            return APIErrorValue("Couldnt find dish").json(500)
        
        quantity_dish2 = 0
        if form_dish['quantity'] != [0]:
                quantity_dish2 = int(form_dish['quantity'])
        else:
            quantity_dish2 = 0
        MealsHandler.add_company_dish(
                company=company, dish=dish, dish_quantity=quantity_dish2
            )
    return ("",204)
        
        # dish_ids_by_type = request.form.getlist("dish_" + dish_type)
        # dish_quantities_by_type = request.form.getlist("dish_quantity_" + dish_type)

        # if dish_ids_by_type is None or dish_quantities_by_type is None:
        #     continue

        # if company_meal.max_dish_quantity is not None:
        #     try:
        #         if (
        #             sum(list(map(int, filter(None, dish_quantities_by_type))))
        #             > company_meal.max_dish_quantity
        #         ):
        #             return APIErrorValue(
        #                 "Number of " + dish_type + "s over maximum value!"
        #             ).json(500)
        #     except Exception as e:
        #         return APIErrorValue("Quantities type not int, " + str(e)).json(500)

        #     for dish_quantity_by_type in dish_quantities_by_type:
        #         if dish_quantity_by_type is not None and not isinstance(
        #             dish_quantity_by_type, int
        #         ):
        #             return APIErrorValue("Quantities type not int").json(500)

    #     dish_ids += dish_ids_by_type
    #     dish_quantities += dish_quantities_by_type

    # if dish_ids:
    #     for index, dish_id in enumerate(dish_ids):
    #         dish = MealsFinder.get_dishes_from_dish_external_id(dish_id)

    #         if dish is None:
    #             return APIErrorValue("Couldnt find dish").json(500)

    #         try:
    #             dish_quantity = int(dish_quantities[index])
    #         except ValueError:
    #             continue
    #         except TypeError:
    #             continue
    #         except IndexError:
    #             return APIErrorValue("Quantities size different from dishes").json(500)

    #         MealsHandler.add_company_dish(
    #             company=company_user.company, dish=dish, dish_quantity=dish_quantity
    #         )

    # return redirect(url_for("companies_api.meals_dashboard"))
