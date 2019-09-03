from flask import session, Response
from functools import wraps
from flask_login import current_user

def require_student_login(func):
    @wraps(func)
    def check_student_login(*args, **kwargs):
        # Check to see if it's in their sessio
        user_role = current_user.get_role()

        if not session['student'] or user_role != "student":
            # If it isn't return our access denied message (you can also return a redirect or render_template)
            return Response("Access denied")

        # Otherwise just send them where they wanted to go
        return func(*args, **kwargs)

    return check_student_login


def require_company_login(func):
    @wraps(func)
    def check_company_login(*args, **kwargs):
        user_role = current_user.get_role()

        if not session['company'] or user_role != "company":
            return Response("Access denied")

        return func(*args, **kwargs)

    return check_company_login


def require_admin_login(func):
    @wraps(func)
    def check_admin_login(*args, **kwargs):
        user_role = current_user.get_role()

        if not session['admin'] or user_role != "admin":
            return Response("Access denied")
        
        return func(*args, **kwargs)

    return check_admin_login