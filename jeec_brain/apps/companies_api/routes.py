from flask import request, render_template, redirect, url_for, session
from jeec_brain.apps.companies_api import bp
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler
from jeec_brain.finders.auctions_finder import AuctionsFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.handlers.users_handler import UsersHandler
from datetime import datetime


@bp.route('/', methods=['GET'])
def get_company_login_form():
    if current_user.is_authenticated and current_user.role == 'company':
        return redirect(url_for('companies_api.dashboard'))

    return render_template('companies/companies_login.html')


@bp.route('/', methods=['POST'])
def company_login():    
    username = request.form.get('username')
    password = request.form.get('password')

    # if credentials are sent in json (for stress testing purposes)
    if not username and not password:
        username = request.json.get('username')
        password = request.json.get('password')

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
def dashboard(company_user):
    if not company_user.user.accepted_terms:
        return render_template('companies/terms_conditions.html', user=company_user.user)

    if company_user.company.cvs_access:
        event = EventsFinder.get_default_event()
        today = datetime.now()
        cvs_access_start = datetime.strptime(event.cvs_access_start, '%d %b %Y, %a')
        cvs_access_end = datetime.strptime(event.cvs_access_end, '%d %b %Y, %a')
        if today < cvs_access_start or today > cvs_access_end:
            cvs_enabled = False
        else:
            cvs_enabled = True
    else:
        cvs_enabled = False

    company_auctions = CompaniesFinder.get_company_auctions(company_user.company)

    company_logo = CompaniesHandler.find_image(company_user.company.name)

    activity_types = []
    for activity in company_user.company.activities:
        if (activity.activity_type not in activity_types) and (activity.activity_type.name != 'Job Fair'):
            activity_types.append(activity.activity_type)

    return render_template('companies/dashboard.html', auctions=company_auctions, company_logo=company_logo, activity_types=activity_types, user=company_user, cvs_enabled=cvs_enabled)


@bp.route('/dashboard', methods=['POST'])
@require_company_login
def accept_terms(company_user):
    UsersHandler.update_user(user=company_user.user, accepted_terms=True)

    return redirect(url_for('companies_api.dashboard'))
