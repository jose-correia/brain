from .. import bp
from flask import render_template, current_app, request, redirect, url_for
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.company_users_handler import CompanyUsersHandler
from jeec_brain.handlers.activities_handler import ActivitiesHandler
from jeec_brain.services.users.get_roles_service import GetRolesService
from jeec_brain.services.users.generate_credentials_service import (
    GenerateCredentialsService,
)
from jeec_brain.apps.auth.wrappers import allowed_roles
from jeec_brain.models.enums.roles_enum import RolesEnum
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.admin_api.users.schemas import *
from flask_login import current_user

from config import Config


# Users routes
@bp.get("/users")
@allowed_roles(["admin"])
def users_dashboard():
    search_parameters = request.args
    username = request.args.get("username")

    # handle search bar requests
    if username is not None:
        search = username
        users_list = UsersFinder.get_admin_users_by_username(username)
        company_users_list = UsersFinder.get_company_users_from_username(username)

    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = "search name"

        users_list = UsersFinder.get_admin_users_from_parameters(search_parameters)
        company_users_list = None

    # request endpoint with no parameters should return all users
    else:
        search = None
        users_list = UsersFinder.get_all_admin_users()
        company_users_list = UsersFinder.get_all_company_users()

    if (users_list is None or len(users_list) == 0) and (
        company_users_list is None or len(company_users_list) == 0
    ):
        error = "No results found"
        return render_template(
            "admin/users/users_dashboard.html",
            users=None,
            company_users=None,
            error=error,
            search=search,
            current_user=current_user,
        )

    return render_template(
        "admin/users/users_dashboard.html",
        users=users_list,
        company_users=company_users_list,
        error=None,
        search=search,
        current_user=current_user,
    )


@bp.get("/new-user")
@allowed_roles(["admin"])
def add_user_dashboard():
    roles = GetRolesService.call()

    if "company" and "student" in roles:
        roles.remove("company")
        roles.remove("student")

    return render_template(
        "admin/users/add_user.html", user=current_user, roles=roles, error=None
    )


@bp.get("/new-organization-user")
@allowed_roles(["admin"])
def add_company_user_dashboard():
    companies = CompaniesFinder.get_all()

    return render_template(
        "admin/users/add_company_user.html",
        user=current_user,
        companies=companies,
        error=None,
    )


@bp.post("/new-user")
@allowed_roles(["admin"])
def create_user():
    # extract form parameters
    name = request.form.get("name")
    username = request.form.get("username")
    email = request.form.get("email", None)
    role = request.form.get("role", None)
    post = request.form.get("post", None)

    # check if is creating company user
    company_external_id = request.form.get("company_external_id")
    if company_external_id is not None:
        company = CompaniesFinder.get_from_external_id(company_external_id)
        company_id = company.id

        if company is None:
            return "No company found", 404

    # extract food_manager from parameters
    food_manager = request.form.get("food_manager", None)

    if food_manager == "True":
        food_manager = True
    elif food_manager == "False":
        food_manager = False
    else:
        food_manager = None

    # create new company user
    if company_external_id:
        company_user = CompanyUsersHandler.create_company_user(
            Config.ROCKET_CHAT_ENABLE,
            name,
            username,
            email,
            company,
            post,
            food_manager,
        )
        if not company_user:
            return render_template(
                "admin/users/add_company_user.html",
                user=current_user,
                companies=CompaniesFinder.get_all(),
                roles=GetRolesService.call(),
                error="Failed to create user!",
            )

    else:
        if role not in GetRolesService.call():
            return "Wrong role type provided", 404
        else:
            role = RolesEnum[role]

        user = UsersHandler.create_user(
            name=name,
            username=username,
            email=email,
            role=role,
            password=GenerateCredentialsService().call(),
        )

        if user is None:
            return render_template(
                "admin/users/add_user.html",
                roles=GetRolesService.call(),
                error="Failed to create user!",
            )

    return redirect(url_for("admin_api.users_dashboard"))


@bp.get("/user/<string:user_external_id>/delete")
@allowed_roles(["admin"])
def delete_user(path: UserPath):
    user = UsersFinder.get_from_external_id(path.user_external_id)

    if user is None:
        return APIErrorValue("Couldnt find user").json(500)

    if user.role.name == "company":
        company_user = UsersFinder.get_company_user_from_user(user)
        if not company_user:
            return APIErrorValue("Couldnt find user").json(500)

        CompanyUsersHandler.delete_company_user(company_user)

    else:
        UsersHandler.delete_user(Config.ROCKET_CHAT_ENABLE, user)

    return redirect(url_for("admin_api.users_dashboard"))


@bp.get("/user/<string:user_external_id>/credentials")
@allowed_roles(["admin"])
def generate_user_credentials(path: UserPath):
    user = UsersFinder.get_from_external_id(path.user_external_id)

    if user is None:
        return APIErrorValue("Couldnt find user").json(500)

    UsersHandler.generate_new_user_credentials(user=user)
    return redirect(url_for("admin_api.companies_dashboard"))
