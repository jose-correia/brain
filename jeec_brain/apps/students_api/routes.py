from flask import request, render_template, redirect, url_for
from jeec_brain.apps.students_api import bp
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_student_login
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler
from jeec_brain.handlers.users_handler import UsersHandler


@bp.route('/', methods=['GET'])
def student_login(): 
    if current_user.is_authenticated and current_user.role == 'student':
        return redirect(url_for('students_api.dashboard'))

    return AuthHandler.redirect_to_fenix_login()


@bp.route('/redirect_uri')
def redirect_uri():
    if request.args.get('error') == "access_denied":
        return redirect(url_for('/'))
    
    fenix_auth_code = request.args.get('code')

    if AuthHandler.login_student(fenix_auth_code) is True:
        return redirect(url_for('students_api.dashboard'))

    else:
        return APIErrorValue("Failed to authenticate!").json(401)


@bp.route('/student-logout', methods=['GET'])
def student_logout():
    try:
        AuthHandler.logout_user()
    except:
        pass
    return redirect(url_for('students_api.get_student_login_form'))


@bp.route('/dashboard', methods=['GET'])
#@require_student_login
def dashboard():
    #if not current_user.accepted_terms:
        #return render_template('students/terms_conditions.html', user=current_user)

    return render_template('students/dashboard.html', user=current_user)


@bp.route('/dashboard', methods=['POST'])
@require_student_login
def accept_terms():
    UsersHandler.update_user(user=current_user, accepted_terms=True)
    return redirect(url_for('students_api.dashboard'))
