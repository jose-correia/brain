from jeec_brain.apps.companies_api import bp
from flask import render_template, session, request, redirect, url_for
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.activity_codes_finder import ActivityCodesFinder
from jeec_brain.handlers.activity_codes_handler import ActivityCodesHandler
from jeec_brain.values.api_error_value import APIErrorValue
from datetime import datetime


@bp.route('/activities', methods=['GET'])
@require_company_login
def activities_dashboard():
    if current_user.company is None:
        return APIErrorValue('Couldnt find company').json(400)

    activities = current_user.company.activities
    if activities is None or len(activities) == 0:
        return render_template('companies/activities/activities_dashboard.html', activities=None, error="No activities found", company=current_user.company)

    return render_template('companies/activities/activities_dashboard.html', activities=activities, error=None, company=current_user.company)


@bp.route('/activity/<string:activity_external_id>', methods=['GET'])
@require_company_login
def get_activity(activity_external_id):
    if current_user.company is None:
        return APIErrorValue('Couldnt find company').json(400)

    activity = ActivitiesFinder.get_from_external_id(activity_external_id)
    if activity is None:
        return APIErrorValue('Couldnt find activity').json(400)

    codes = ActivityCodesFinder.get_from_parameters({'activity_id':activity.id})

    return render_template('companies/activities/activity.html', \
        activity=activity, \
        error=None, \
        codes=codes, \
        user=current_user)


@bp.route('/activity/<string:activity_external_id>/code', methods=['POST'])
@require_company_login
def create_activity_code(activity_external_id):
    if current_user.company is None:
        return APIErrorValue('Couldnt find company').json(400)
    
    activity = ActivitiesFinder.get_from_external_id(activity_external_id)
    if activity is None:
        return APIErrorValue('Couldnt find activity').json(400)
    
    codes = []
    number_of_codes = request.form.get("number", 1)
    
    i = 0
    while i < number_of_codes:
        activity_code = ActivityCodesHandler.create_activity_code(activity_id=activity.id)
        codes.append(activity_code.code)
        i = i + 1

    return render_template('companies/activities/activity.html', \
        activity=activity, \
        error=None, \
        codes=codes, \
        user=current_user)