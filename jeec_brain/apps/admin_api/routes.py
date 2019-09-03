from flask import request, render_template, session, redirect, url_for, current_app
from . import bp

from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_admin_login
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler


@bp.route('/admin-login', methods=['GET'])
def get_admin_login_form():
    if current_user.is_authenticated and session.get('admin'):
        return redirect(url_for('admin_api.dashboard'))
    return render_template('admin/admin_login.html')


@bp.route('/admin-login', methods=['POST'])
def login():
    if session.get('admin'):
        return redirect(url_for('admin_bp.dashboard'))
    
    username = request.form.get('username')
    password = request.form.get('password')

    if AuthHandler.login_admin(username, password) is False:
        return render_template('admin_login.html', error="Invalid credentials!")

    return redirect(url_for('admin_api.dashboard'))


# content routes
@bp.route('/dashboard', methods=['GET'])
@require_admin_login
def dashboard():
    return render_template('admin/dashboard.html')

