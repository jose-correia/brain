from . import bp
from flask import render_template, current_app, request, redirect, url_for, make_response, session, jsonify
from flask_login  import current_user, login_required
from config import Config

# Handlers
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler
from jeec_brain.apps.auth.wrappers import require_student_login

# Finders
from jeec_brain.finders.students_finder import StudentsFinder

# Values
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.values.student_value import StudentValue

# Login routes
@bp.route('/login')
def login_student():
    return AuthHandler.redirect_to_fenix_login()

@bp.route('/redirect_uri')
def redirect_uri():
    if request.args.get('error') == "access_denied":
        return redirect(Config.STUDENT_APP_URL + 'login')
    
    fenix_auth_code = request.args.get('code')

    loggedin, jwt = AuthHandler.login_student(fenix_auth_code)
    
    if loggedin is True:
        return redirect(Config.STUDENT_APP_URL + 'login?jwt=' + str(jwt, 'utf-8'))

    else:
        return redirect(Config.STUDENT_APP_URL)

@bp.route('/logout', methods=['POST'])
@require_student_login
def logout():
    AuthHandler.logout_user()

    return jsonify("User successfully logged out"), 200

@bp.route('/info', methods=['GET'])
def get_info():
    user = current_user
    if(user.is_anonymous):
        return APIErrorValue('No user found').json(401)

    student = StudentsFinder.get_from_user_id(user.id)
    
    return StudentValue(student, details=False).json(200)