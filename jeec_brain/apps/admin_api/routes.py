from flask import request, render_template, session, redirect, url_for
from . import bp

from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_admin_login
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler

import logging
logger = logging.getLogger(__name__)


@bp.route('/', methods=['GET'])
def get_admin_login_form():
    if current_user.is_authenticated:
        return redirect(url_for('admin_api.dashboard'))

    return render_template('admin/admin_login.html')


@bp.route('/', methods=['POST'])
def admin_login():    
    username = request.form.get('username')
    password = request.form.get('password')

    if AuthHandler.login_admin(username, password) is False:
        return render_template('admin/admin_login.html', error="Invalid credentials!")

    return render_template('admin/dashboard.html')


# content routes
@bp.route('/admin-logout', methods=['GET'])
@require_admin_login
def admin_logout():
    AuthHandler.logout_admin()
    return redirect(url_for('admin_api.get_admin_login_form'))


# content routes
@bp.route('/dashboard', methods=['GET'])
@require_admin_login
def dashboard():
    return render_template('admin/dashboard.html')

