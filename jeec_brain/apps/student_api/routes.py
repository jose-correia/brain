from . import bp
from flask import render_template, current_app, request, redirect, url_for, make_response, session, jsonify
from flask_login  import current_user, login_required
from config import Config

# Handlers
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler
from jeec_brain.apps.auth.wrappers import require_student_login
from jeec_brain.handlers.activity_codes_handler import ActivityCodesHandler
from jeec_brain.handlers.students_handler import StudentsHandler

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
        return redirect(Config.STUDENT_APP_URL + '?jwt=' + str(jwt, 'utf-8'))

    else:
        return redirect(Config.STUDENT_APP_URL)

@bp.route('/info', methods=['GET'])
def get_info():
    user = current_user
    if(user.is_anonymous):
        return APIErrorValue('No user found').json(401)

    student = StudentsFinder.get_from_user_id(user.id)
    if(student is None):
        return APIErrorValue('No user found').json(401)
    
    return StudentValue(student, details=False).json(200)

@bp.route('/redeem-code', methods=['POST'])
def redeem_code():
    user = current_user
    if(user.is_anonymous):
        return APIErrorValue('No user found').json(401)

    student = StudentsFinder.get_from_user_id(user.id)
    if(student is None):
        return APIErrorValue('No user found').json(401)

    try:
        code = request.get_json()["code"]
    except KeyError:
        return APIErrorValue('Invalid code').json(500)

    student = ActivityCodesHandler.redeem_activity_code(student, code)

    if(student is None):
        return APIErrorValue('Invalid code').json(500)

    return StudentValue(student, details=False).json(200)

@bp.route('/add-linkedin', methods=['POST'])
def add_linkedin():
    user = current_user
    if(user.is_anonymous):
        return APIErrorValue('No user found').json(401)

    student = StudentsFinder.get_from_user_id(user.id)
    if(student is None):
        return APIErrorValue('No user found').json(401)

    try:
        url = request.get_json()["url"]
    except KeyError:
        return APIErrorValue('Invalid url').json(500)

    student = StudentsHandler.add_linkedin(student, url)

    return StudentValue(student, details=False).json(200)