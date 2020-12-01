from flask import session, Response, redirect, url_for, request
import os
import base64
from functools import wraps
from flask_login import current_user
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.apps.auth.services.decode_jwt_service import DecodeJwtService


def require_student_login(func):
    @wraps(func)
    def check_student_login(*args, **kwargs):

        # Check to see if it's in their session
        print(session['name'] if session.get('name') else "None")
        if current_user.is_anonymous:
            # If it isn't return our access denied message (you can also return a redirect or render_template)
            return Response("Access denied", status=401)

        # Otherwise just send them where they wanted to go
        return func(*args, **kwargs)

    return check_student_login


def require_company_login(func):
    @wraps(func)
    def check_company_login(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role.name is not 'company':
            return Response("Access denied", status=401)

        return func(*args, **kwargs)
    return check_company_login


def allowed_roles(role_names):
    def wrapper(view_function):
        @wraps(view_function)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated:
                return Response("Access denied", status=401)
            
            user = UsersFinder.get_user_from_username(current_user.username)

            if user is None or current_user.role.name not in role_names:
                return Response("Access denied", status=401)

            return view_function(*args, **kwargs)
        return decorated
    return wrapper


def allow_all_roles(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return Response("Access denied", status=401)
        
        if current_user.role.name not in ['admin', 'companies_admin', 'speakers_admin', 'teams_admin', 'activities_admin', 'viewer']:
            return Response("Access denied", status=401)

        return func(*args, **kwargs)
    return decorated
	

def requires_client_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        http_auth = request.environ.get('HTTP_AUTHORIZATION')

        if http_auth:
            auth_type, data = http_auth.split(' ', 1)

            if auth_type == 'Basic':
                auth_string = os.environ.get('CLIENT_USERNAME') + ':' + os.environ.get('CLIENT_KEY')
                auth_bytes = auth_string.encode("utf-8")

                if data.encode("utf-8") == base64.b64encode(auth_bytes): 
                    return func(*args, **kwargs)
        return Response("Access denied", status=401)
    return decorated

def requires_student_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        user = current_user
        if(user.is_anonymous):
            return Response("No user found, access denied", status=401)

        student = StudentsFinder.get_from_user_id(user.id)
        if(student is None):
            return Response("No student found, access denied", status=401)
            
        return func(*args, student=student)
    return decorated