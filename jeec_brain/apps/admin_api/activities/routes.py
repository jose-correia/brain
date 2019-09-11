from .. import bp
from flask import render_template, current_app, request, redirect, url_for
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.speakers_finder import SpeakersFinder
from jeec_brain.handlers.activities_handler import ActivitiesHandler
from jeec_brain.services.activities.get_activity_types_service import GetActivityTypesService
from jeec_brain.apps.auth.wrappers import require_admin_login


# Activities routes
@bp.route('/activities', methods=['GET'])
@require_admin_login
def activities_dashboard():
    activity_types = GetActivityTypesService.call()
    search_parameters = request.args
    name = request.args.get('name')

    # handle search bar requests
    if name is not None:
        search = name
        activities_list = ActivitiesFinder.search_by_name(name)
    
    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = None

        activities_list = ActivitiesFinder.get_from_parameters(search_parameters)

    # request endpoint with no parameters should return all activities
    else:
        search = None
        activities_list = ActivitiesFinder.get_all()
    
    if activities_list is None or len(activities_list) == 0:
        error = 'No results found'
        return render_template('admin/activities/activities_dashboard.html', activities=None, activity_types=activity_types, error=error, search=search)

    return render_template('admin/activities/activities_dashboard.html', activities=activities_list, activity_types=activity_types, error=None, search=search)


@bp.route('/new-activity', methods=['GET'])
@require_admin_login
def add_activity_dashboard():
    activity_type = request.args.get('type')
    
    if activity_type not in GetActivityTypesService.call():
        return 'Wrong activity type provided', 404

    companies = CompaniesFinder.get_all()
    speakers = SpeakersFinder.get_all()

    return render_template('admin/activities/add_activity.html', \
        type=activity_type, \
        companies=companies, \
        speakers=speakers, \
        error=None)


@bp.route('/new-activity', methods=['POST'])
@require_admin_login
def create_activity():
    activity_type = request.args.get('type')
    if activity_type not in GetActivityTypesService.call():
        return 'Wrong activity type provided', 404

    # extract form parameters
    name = request.form.get('name')
    description = request.form.get('description')
    location = request.form.get('location')
    day = request.form.get('day')
    time = request.form.get('time')
    registration_link = request.form.get('registration_link')
    registration_open = request.form.get('registration_open')

    if registration_open == 'True':
        registration_open = True
    else:
        registration_open = False

    # create new activity
    activity = ActivitiesHandler.create_activity(
            name=name,
            description=description,
            type=activity_type,
            location=location,
            day=day,
            time=time,
            registration_link=registration_link,
            registration_open=registration_open
        )

    if activity is None:
        companies = CompaniesFinder.get_all()
        speakers = SpeakersFinder.get_all()
        return render_template('admin/activities/add_activity.html', \
            type=activity_type, \
            companies=companies, \
            speakers=speakers, \
            error="Failed to create activity! Maybe it already exists :)")

    # extract company names and speaker names from parameters
    companies = request.form.getlist('company')
    speakers = request.form.getlist('speaker')

    # if company names where provided
    if companies:
        for name in companies:
            company = CompaniesFinder.get_from_name(name)
            if company is None:
                return APIErrorValue('Couldnt find company').json(500)

            company_activity = CompaniesHandler.add_activity(company, activity)
            if company_activity is None:
                return APIErrorValue('Failed to create company activity').json(500)

    if speakers:
        for name in speakers:
            speaker = SpeakersFinder.get_from_name(name)
            if speaker is None:
                return APIErrorValue('Couldnt find speaker').json(500)

            speaker_activity = SpeakersHandler.add_activity(speaker, activity)
            if speaker_activity is None:
                return APIErrorValue('Failed to create speaker activity').json(500)

    return redirect(url_for('admin_api.activities_dashboard'))


@bp.route('/activity/<string:activity_external_id>', methods=['GET'])
@require_admin_login
def get_activity(activity_external_id):
    activity = ActivitiesFinder.get_from_external_id(activity_external_id)

    return render_template('admin/activities/update_activity.html', activity=activity, error=None)


@bp.route('/activity/<string:activity_external_id>', methods=['POST'])
@require_admin_login
def update_activity(activity_external_id):

    activity = ActivitiesFinder.get_from_external_id(activity_external_id)

    if activity is None:
        return APIErrorValue('Couldnt find activity').json(500)

    # extract form parameters
    name = request.form.get('name')
    description = request.form.get('description')
    location = request.form.get('location')
    day = request.form.get('day')
    time = request.form.get('time')
    registration_link = request.form.get('registration_link')
    registration_open = request.form.get('registration_open')

    if registration_open == 'True':
        registration_open = True
    else:
        registration_open = False

    updated_activity = ActivitiesHandler.update_activity(
        activity=activity,
        name=name,
        description=description,
        location=location,
        day=day,
        time=time,
        registration_link=registration_link,
        registration_open=registration_open
    )
    
    if updated_activity is None:
        return render_template('admin/activities/update_activity.html', activity=activity, error="Failed to update activity!")

    return redirect(url_for('admin_api.activities_dashboard'))


@bp.route('/activity/<string:activity_external_id>/delete', methods=['GET'])
@require_admin_login
def delete_activity(activity_external_id):
    activity = ActivitiesFinder.get_from_external_id(activity_external_id)

    if activity is None:
        return APIErrorValue('Couldnt find activity').json(500)
        
    if ActivitiesHandler.delete_activity(activity):
        return redirect(url_for('admin_api.activities_dashboard'))

    else:
        return render_template('admin/activities/update_activity.html', activity=activity, error="Failed to delete activity!")
