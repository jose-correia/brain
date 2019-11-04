from flask import request, render_template, redirect, url_for, session
from jeec_brain.apps.companies_api import bp
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler
from jeec_brain.finders.auctions_finder import AuctionsFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler


@bp.route('/', methods=['GET'])
def get_company_login_form():
    if current_user.is_authenticated and current_user.role == 'company':
        return redirect(url_for('companies_api.dashboard'))

    return render_template('companies/companies_login.html')


@bp.route('/', methods=['POST'])
def company_login():    
    username = request.form.get('username')
    password = request.form.get('password')

    if AuthHandler.login_company(username, password) is False:
        return render_template('companies/companies_login.html', error="Invalid credentials!")

    return redirect(url_for('companies_api.dashboard'))


@bp.route('/company-logout', methods=['GET'])
def company_logout():
    try:
        AuthHandler.logout_user()
    except:
        pass
    return redirect(url_for('companies_api.get_company_login_form'))


@bp.route('/dashboard', methods=['GET'])
@require_company_login
def dashboard():
    company_auctions = CompaniesFinder.get_company_auctions(current_user.company)

    company_logo = CompaniesHandler.find_image(current_user.company.name)

    return render_template('companies/dashboard.html', auctions=company_auctions, company_logo=company_logo, user=current_user)

