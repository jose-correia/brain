import os
from flask import send_file, Response, render_template, session, redirect, url_for, render_template, request
from .. import bp

from jeec_brain.handlers.file_handler import FileHandler
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler

import logging
logger = logging.getLogger(__name__)


# Company Login
@bp.route('/company-login', methods=['POST'])
def login_company():
    if current_user.is_authenticated:
        return redirect(url_for('cv_platform_api.dashboard'))

    username = request.form['username']
    password = request.form['password']

    if AuthHandler.login_company(username, password) is False:
        return render_template('company_login.html', error="Invalid credentials!")

    return redirect(url_for('cv_platform_api_bp.company_dashboard'))


@bp.route('/company-login', methods=['GET'])
def get_company_login_form():
    if current_user.is_authenticated:
        return redirect(url_for('cv_platform_api_bp.company_dashboard'))
        
    return render_template('company_login.html')


# route for the company dashboard
@bp.route('/company_dashboard', methods=['GET'])
@require_company_login
def company_dashboard():
    logger.info('entered dashboard!')
    company_name = session['name']
    company_logo = '/static/companies/' + company_name.lower() + '.png'

    return render_template('company_dashboard.html', name=company_name, logo=company_logo)
        

