from flask import request, redirect, session, url_for, render_template
from . import bp, client
import json
import os
from .handlers.tecnico_client_handler import TecnicoClientHandler
from .handlers.auth_handler import AuthHandler
from flask_login import current_user, login_user, logout_user
from .finders.company_finder import CompanyFinder

import logging
logger = logging.getLogger(__name__)

#student login
@bp.route('/login')
def login():
   
    url = TecnicoClientHandler.get_authentication_url(client)
    
    return redirect(url, code=302)

@bp.route('/redirect_uri')
def redirect_uri():
    if request.args.get('error') == "access_denied":
        return redirect(url_for('/'))
    
    fenix_auth_code = request.args.get('code')

    if fenix_auth_code is not None:
        session['fenix_auth_code'] = fenix_auth_code
        
        user = TecnicoClientHandler.get_user(client, fenix_auth_code)
        person = TecnicoClientHandler.get_person(client, user)
    
        session['name'] = person['name']
        session['username'] = person['username']
        session['first_time_login'] = False

        if AuthHandler.check_for_user() is False:
            logger.info("New user created.")
            
        logger.info('User authenticated!')

        return redirect(url_for('cv_platform_api_bp.student_dashboard'))
    
    else:
        return redirect(url_for('/'))
    

@bp.route('/logout', methods=['GET'])
def logout():
    session.pop('fenix_auth_code', None)
    session.pop('name', None)
    session.pop('username', None)
    return redirect(url_for('cv_platform_api_bp.index'))

@bp.route('/company-login', methods=['POST'])
def login_company():
    if current_user.is_authenticated:
        return redirect(url_for('cv_platform_api.dashboard'))

    username = request.form['username']
    password = request.form['password']

    company = CompanyFinder.get_from_username(username=username)

    if company is None or not company.check_password(password):
        logger.error("Company tried to login with invalid credentials!")
        return render_template('company_login.html', error="Invalid credentials!")

    login_user(company)
    session['name'] = company.name
    return redirect(url_for('cv_platform_api_bp.company_dashboard'))


@bp.route('/company-login', methods=['GET'])
def get_company_login_form():
    if current_user.is_authenticated:
        return redirect(url_for('cv_platform_api_bp.company_dashboard'))
        
    return render_template('company_login.html')

@bp.route('/company-logout')
def company_logout():
    logout_user()
    return redirect(url_for('cv_platform_api_bp.index'))

# @bp.route('/company_registration', methods=['POST'])
# def register_compamny():
#     username = request.json.get('username')
#     password = request.json.get('password')

#     if username is None or password is None:
#         abort(400) # missing arguments to auth
#     if CompanyFinder.get_by_username(username) is not None:
#         abort(400) # company already exists
    
#     company = Company(username=username)
#     company.hash_password(password)
#     db.session.add(company)
#     db.session.commmit()

#     return redirect('/')