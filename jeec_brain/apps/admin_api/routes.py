from flask import request, render_template, session, redirect, url_for, make_response
from . import bp

from flask_login import current_user
from jeec_brain.apps.auth.wrappers import allow_all_roles
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler

import logging
logger = logging.getLogger(__name__)


@bp.route('/', methods=['GET'])
def get_admin_login_form():
    if current_user.is_authenticated and current_user.role.name in ['admin', 'companies_admin', 'speakers_admin', 'teams_admin', 'activities_admin', 'viewer']:
        return redirect(url_for('admin_api.dashboard'))

    return render_template('admin/admin_login.html')


@bp.route('/', methods=['POST'])
def admin_login():    
    username = request.form.get('username')
    password = request.form.get('password')

    if AuthHandler.login_admin_dashboard(username, password) is False:
        return render_template('admin/admin_login.html', error="Invalid credentials!")

    return redirect(url_for('admin_api.dashboard'))


# content routes
@bp.route('/admin-logout', methods=['GET'])
def admin_logout():
    try:
        AuthHandler.logout_user()
    except:
        pass
    return redirect(url_for('admin_api.get_admin_login_form'))


# content routes
@bp.route('/dashboard', methods=['GET'])
@allow_all_roles
def dashboard():
    return render_template('admin/dashboard.html', role=current_user.role.name)

