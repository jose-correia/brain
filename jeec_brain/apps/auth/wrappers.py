from flask import session, Response, redirect, url_for, request
import os
import base64
from functools import wraps
from flask_login import current_user


def require_student_login(func):
    @wraps(func)
    def check_student_login(*args, **kwargs):
        # Check to see if it's in their sessio
        user_role = current_user.get_role()

        if not session['student'] or user_role != "student":
            # If it isn't return our access denied message (you can also return a redirect or render_template)
            return Response("Access denied", status=401)

        # Otherwise just send them where they wanted to go
        return func(*args, **kwargs)

    return check_student_login


def require_company_login(func):
    @wraps(func)
    def check_company_login(*args, **kwargs):
        user_role = current_user.get_role()

        if not session['company'] or user_role != "company":
            return Response("Access denied", status=401)

        return func(*args, **kwargs)

    return check_company_login


def require_admin_login(func):
    @wraps(func)
    def check_admin_login(*args, **kwargs):
        try:
            if session['admin'] != 'True':
                return redirect('https://www.google.pt/')
        except Exception as e:
            raise e

        return func(*args, **kwargs)

    return check_admin_login


def requires_client_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        http_auth = request.environ.get('HTTP_AUTHORIZATION')

        if http_auth:
            auth_type, data = http_auth.split(' ', 1)

            username = None
            api_key = None

            if auth_type == 'Basic':
                auth_string = os.environ.get('CLIENT_USERNAME') + ':' + os.environ.get('CLIENT_KEY')
                auth_bytes = auth_string.encode("utf-8")

                if data.encode("utf-8") == base64.b64encode(auth_bytes): 
                    return func(*args, **kwargs)
        return Response("Access denied", status=401)
    return decorated