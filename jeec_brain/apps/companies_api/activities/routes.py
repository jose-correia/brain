from jeec_brain.apps.companies_api import bp
from flask import render_template, session, request, redirect, url_for, jsonify
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.activity_types_finder import ActivityTypesFinder
from jeec_brain.finders.activity_codes_finder import ActivityCodesFinder
from jeec_brain.handlers.activity_codes_handler import ActivityCodesHandler
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.companies_api.activities.schemas import *
from datetime import datetime
from config import Config

@bp.get('/activities')
@require_company_login
def activities_dashboard(company_user):
    activities = company_user.company.activities
    if activities is None or len(activities) == 0:
        return render_template('companies/activities/activities_dashboard.html', activities=None, error="No activities found", company=company_user.company)

    return render_template('companies/activities/activities_dashboard.html', activities=activities, error=None, company=company_user.company)


@bp.get('/activity/<string:activity_external_id>')
@require_company_login
def get_activity(company_user, path: ActivityPath):
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    if activity is None:
        return APIErrorValue('Couldnt find activity').json(400)

    codes = ActivityCodesFinder.get_from_parameters({'activity_id':activity.id})

    return render_template('companies/activities/activity.html', \
        activity=activity, \
        error=None, \
        codes=codes, \
        user=company_user)

@bp.get('/activity_type/<string:activity_type_external_id>')
@require_company_login
def get_activity_type(company_user, path: ActivityTypePath):
    activity_type = ActivityTypesFinder.get_from_external_id(path.activity_type_external_id)
    if activity_type is None:
        return APIErrorValue("No activity type found").json(404)

    activities = []
    for activity in company_user.company.activities:
        if activity.activity_type == activity_type:
            _activity = dict(ActivitiesFinder.get_from_external_id(activity.external_id).__dict__)
            _activity['external_id'] = _activity['external_id'].hex
            _activity.pop('_sa_instance_state')
            _activity.pop('created_at')
            _activity.pop('chat_type')
            activities.append(_activity)

    now = datetime.utcnow()
    today = now.strftime('%d %b %Y, %a')
    for _ in range(len(activities)):
        if activities[0]['day'] == today:
            break
        activities.append(activities.pop(0))

    return render_template('companies/activities/activity_type.html', \
        activities=activities, \
        activity_type=activity_type, \
        error=None, \
        user=company_user)

@bp.get('/job_fair')
@require_company_login
def get_job_fair(company_user):
    job_fairs = []
    for activity in ActivitiesFinder.get_current_company_activities(company_user.company):
        if activity.activity_type.name == 'Job Fair Booth':
            _activity = dict(ActivitiesFinder.get_from_external_id(activity.external_id).__dict__)
            _activity['external_id'] = _activity['external_id'].hex
            _activity.pop('_sa_instance_state')
            _activity.pop('created_at')
            _activity.pop('chat_type')
            job_fairs.append(_activity)

    if len(job_fairs) == 0:
        return APIErrorValue("Job Fair not found").json(404)

    now = datetime.utcnow()
    today = now.strftime('%d %b %Y, %a')
    if today not in [activity['day'] for activity in job_fairs]:
        generate_code = False
    else:
        generate_code = True

    chat_token = UsersHandler.get_chat_user_token(company_user.user)
    chat_url = Config.ROCKET_CHAT_APP_URL + 'home?resumeToken=' + chat_token
    
    return render_template('companies/activities/job_fair.html', \
        generate_code = generate_code, \
        chat_url = chat_url, \
        job_fairs=job_fairs, \
        error=None, \
        user=company_user)

@bp.post('/activity/code')
@require_company_login
def generate_code(company_user):
    now = datetime.utcnow()
    today = now.strftime('%d %b %Y, %a')

    for activity in ActivitiesFinder.get_current_company_activities(company_user.company):
        if activity.activity_type.name == 'Job Fair Booth' and activity.day == today:
            activity_code = ActivityCodesHandler.create_activity_code(activity_id=activity.id)

            return jsonify(activity_code.code)
    
    return APIErrorValue("Not allowed").json(401)