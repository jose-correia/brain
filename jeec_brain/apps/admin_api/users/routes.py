from .. import bp
from flask import render_template, current_app, request, redirect, url_for
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.services.users.get_roles_service import GetRolesService
from jeec_brain.apps.auth.wrappers import allowed_roles
from jeec_brain.models.enums.roles_enum import RolesEnum
from flask_login import current_user


# Users routes
@bp.route('/users', methods=['GET'])
@allowed_roles(['admin'])
def users_dashboard():
    roles = GetRolesService.call()
    search_parameters = request.args
    username = request.args.get('username')

    # handle search bar requests
    if username is not None:
        search = username
        users_list = UsersFinder.search_by_username(username)
    
    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = 'search name'

        users_list = UsersFinder.get_from_parameters(search_parameters)

    # request endpoint with no parameters should return all users
    else:
        search = None
        users_list = UsersFinder.get_all()
    
    if users_list is None or len(users_list) == 0:
        error = 'No results found'
        return render_template('admin/users/users_dashboard.html', users=None, error=error, search=search, current_user=current_user)

    return render_template('admin/users/users_dashboard.html', users=users_list, error=None, search=search, current_user=current_user)


@bp.route('/new-user', methods=['GET'])
@allowed_roles(['admin'])
def add_user_dashboard():
    roles = GetRolesService.call()

    return render_template('admin/users/add_user.html', \
        roles = roles, \
        error=None)


@bp.route('/new-user', methods=['POST'])
@allowed_roles(['admin'])
def create_user():
    # extract form parameters
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    if role not in GetRolesService.call():
        return 'Wrong role type provided', 404
    else:
        role = RolesEnum[role]

    # create new user
    user = UsersHandler.create_user(
            username=username,
            password=password,
            role=role
        )

    if user is None:
        return render_template('admin/users/add_user.html', \
            roles=GetRolesService.call(), \
            error="Failed to create user!")

    return redirect(url_for('admin_api.users_dashboard'))


@bp.route('/user/<string:user_external_id>/delete', methods=['GET'])
@allowed_roles(['admin'])
def delete_user(user_external_id):
    user = UsersFinder.get_from_external_id(user_external_id)

    if user is None:
        return APIErrorValue('Couldnt find user').json(500)
        
    UsersHandler.delete_user(user)
    return redirect(url_for('admin_api.users_dashboard'))
