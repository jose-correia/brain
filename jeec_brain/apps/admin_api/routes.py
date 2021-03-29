from flask import request, render_template, session, redirect, url_for, make_response
from . import bp

from flask_login import current_user
from jeec_brain.apps.auth.wrappers import allow_all_roles
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.handlers.events_handler import EventsHandler

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

    # if credentials are sent in json (for stress testing purposes)
    if not username and not password:
        username = request.json.get('username')
        password = request.json.get('password')

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
    event = EventsFinder.get_default_event()
    if(event is None):
        return render_template('admin/dashboard.html', event=None, logo=None, user=current_user)

    logo = EventsHandler.find_image(image_name=str(event.external_id))
    return render_template('admin/dashboard.html', event=event, logo=logo, user=current_user)

