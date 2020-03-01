from .. import bp
import uuid
from flask import render_template, current_app, request, redirect, url_for
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.activity_types_finder import ActivityTypesFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.speakers_finder import SpeakersFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.handlers.activities_handler import ActivitiesHandler
from jeec_brain.handlers.activity_types_handler import ActivityTypesHandler
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
from flask_login import current_user
from datetime import datetime


# Activities routes
@bp.route('/activities', methods=['GET'])
@allow_all_roles
def activities_dashboard():
    search_parameters = request.args
    name = request.args.get('name')

    # get default event
    event = EventsFinder.get_from_parameters({"default": True})

    if event is None or len(event) == 0:
        error = 'No default event found! Please set a default event in the menu "Events"'
        return render_template('admin/activities/activities_dashboard.html', event=None, activities=None, error=error, search=search, role=current_user.role.name)

    # handle search bar requests
    if name is not None:
        search = name
        activities_list = ActivitiesFinder.search_by_name(name)
    
    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = 'search name'
        
        if 'type' in search_parameters:
            type_external_id = search_parameters['type']
            activity_type = ActivityTypesFinder.get_from_external_id(uuid.UUID(type_external_id))
            activities_list = ActivitiesFinder.get_all_from_type(activity_type)

    # request endpoint with no parameters should return all activities
    else:
        search = None
        activities_list = event[0].activities
    
    if not activities_list:
        error = 'No results found'
        return render_template('admin/activities/activities_dashboard.html', event=event[0], activities=None, error=error, search=search, role=current_user.role.name)

    return render_template('admin/activities/activities_dashboard.html', event=event[0], activities=activities_list, error=None, search=search, role=current_user.role.name)


# Activities Types routes
@bp.route('/activities/types', methods=['GET'])
@allow_all_roles
def activity_types_dashboard():
    event = EventsFinder.get_from_parameters({"default": True})
    
    if event is None or len(event) == 0:
        error = 'No default event found! Please set a default event in the menu "Events"'
        return render_template('admin/activities/activities_dashboard.html', event=None, error=error, role=current_user.role.name)
    
    return render_template('admin/activities/activity_types_dashboard.html', event=event[0], error=None, role=current_user.role.name)


@bp.route('/new-activity-type', methods=['GET'])
@allowed_roles(['admin', 'activities_admin'])
def add_activity_type_dashboard():
    event = EventsFinder.get_from_parameters({"default": True})
    if event is None:
        return APIErrorValue('No default event found! Please set a default event in the menu "Events"').json(500)

    return render_template('admin/activities/add_activity_type.html', event=event[0], error=None)


@bp.route('/new-activity-type', methods=['POST'])
@allowed_roles(['admin', 'activities_admin'])
def create_activity_type():
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')

    event = EventsFinder.get_from_parameters({"default": True})
    if event is None:
        return APIErrorValue('No default event found! Please set a default event in the menu "Events"').json(500)

    activity_type = ActivityTypesHandler.create_activity_type(
            event=event[0],
            name=name,
            description=description,
            price=price
        )

    if activity_type is None:
        return render_template('admin/activities/add_activity_type.html',
            event=event,
            error="Failed to create activity type! Maybe it already exists :)")

    return redirect(url_for('admin_api.activity_types_dashboard'))


@bp.route('/activities/types/<string:activity_type_external_id>', methods=['GET'])
@allowed_roles(['admin', 'activities_admin'])
def get_activity_type(activity_type_external_id):
    activity_type = ActivityTypesFinder.get_from_external_id(activity_type_external_id)

    return render_template('admin/activities/update_activity_type.html', \
        activity_type=activity_type,
        error=None)


@bp.route('/activities/types/<string:activity_type_external_id>', methods=['POST'])
@allowed_roles(['admin', 'activities_admin'])
def update_activity_type(activity_type_external_id):
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')

    activity_type = ActivityTypesFinder.get_from_external_id(activity_type_external_id)

    updated_activity_type = ActivityTypesHandler.update_activity_type(
        activity_type=activity_type,
        name=name,
        description=description,
        price=price
    )

    if updated_activity_type is None:
        return render_template('admin/activities/update_activity_type.html',
            activity_type=activity_type,
            error="Failed to update activity type!")

    return redirect(url_for('admin_api.activity_types_dashboard'))

@bp.route('/activities/types/<string:activity_type_external_id>/delete', methods=['GET'])
@allowed_roles(['admin', 'activities_admin'])
def delete_activity_type(activity_type_external_id):
    activity_type = ActivityTypesFinder.get_from_external_id(activity_type_external_id)

    if activity_type.activities:
        for activity in activity_type.activities:
            if activity is None:
                return APIErrorValue('Couldnt find activity').json(500)
            
            company_activities = ActivitiesFinder.get_company_activities_from_activity_id(activity.external_id)
            speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(activity.external_id)

            if company_activities:
                for company_activity in company_activities:
                    ActivitiesHandler.delete_company_activities(company_activity)

            if speaker_activities:
                for speaker_activity in speaker_activities:
                    ActivitiesHandler.delete_speaker_activities(speaker_activity)

            if not ActivitiesHandler.delete_activity(activity):
                return APIErrorValue('Couldnt delete activity').json(500)
                
    if ActivityTypesHandler.delete_activity_type(activity_type):
        return redirect(url_for('admin_api.activity_types_dashboard'))

    return render_template('admin/activities/update_activity_type.html',
            activity_type=activity_type,
            error="Failed to update activity type!")

@bp.route('/new-activity', methods=['GET'])
@allowed_roles(['admin', 'activities_admin'])
def add_activity_dashboard():
    companies = CompaniesFinder.get_all()
    speakers = SpeakersFinder.get_all()

    event = EventsFinder.get_from_parameters({"default": True})
    
    if event is None or len(event) == 0:
        error = 'No default event found! Please set a default event in the menu "Events"'
        return render_template('admin/activities/activities_dashboard.html', event=None, error=error, role=current_user.role.name)
    
    activity_types = event[0].activity_types

    return render_template('admin/activities/add_activity.html', \
        activity_types = activity_types, \
        companies=companies, \
        speakers=speakers, \
        minDate=datetime.strptime(event[0].start_date,'%d %b %Y, %a').strftime("%Y,%m,%d"), \
        maxDate=datetime.strptime(event[0].end_date,'%d %b %Y, %a').strftime("%Y,%m,%d"), \
        error=None)


@bp.route('/new-activity', methods=['POST'])
@allowed_roles(['admin', 'activities_admin'])
def create_activity():
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

    activity_type_external_id = request.form.get('type')
    activity_type = ActivityTypesFinder.get_from_external_id(uuid.UUID(activity_type_external_id))
    event = activity_type.event

    if event is None:
        error = 'No default event found! Please set a default event in the menu "Events"'
        return render_template('admin/activities/activities_dashboard.html', event=None, error=error, role=current_user.role.name)

    activity = ActivitiesHandler.create_activity(
            name=name,
            description=description,
            activity_type=activity_type,
            event=event,
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
            minDate=datetime.strptime(event.start_date,'%d %b %Y, %a').strftime("%Y,%m,%d"), \
            maxDate=datetime.strptime(event.end_date,'%d %b %Y, %a').strftime("%Y,%m,%d"), \
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

            company_activity = ActivitiesHandler.add_company_activity(company, activity)
            if company_activity is None:
                return APIErrorValue('Failed to create company activity').json(500)

    if speakers:
        for name in speakers:
            speaker = SpeakersFinder.get_from_name(name)
            if speaker is None:
                return APIErrorValue('Couldnt find speaker').json(500)

            speaker_activity = ActivitiesHandler.add_speaker_activity(speaker, activity)
            if speaker_activity is None:
                return APIErrorValue('Failed to create speaker activity').json(500)

    return redirect(url_for('admin_api.activities_dashboard'))


@bp.route('/activity/<string:activity_external_id>', methods=['GET'])
@allowed_roles(['admin', 'activities_admin'])
def get_activity(activity_external_id):
    activity = ActivitiesFinder.get_from_external_id(activity_external_id)
    companies = CompaniesFinder.get_all()
    speakers = SpeakersFinder.get_all()

    event = EventsFinder.get_from_parameters({"default": True})
    if event is None or len(event) == 0:
        error = 'No default event found! Please set a default event in the menu "Events"'
        return render_template('admin/activities/activities_dashboard.html', event=None, error=error, role=current_user.role.name)
    
    activity_types = event[0].activity_types
    company_activities = ActivitiesFinder.get_company_activities_from_activity_id(activity_external_id)
    speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(activity_external_id)

    return render_template('admin/activities/update_activity.html', \
        activity=activity, \
        activity_types=activity_types, \
        companies=companies, \
        speakers=speakers, \
        company_activities=[company.company_id for company in company_activities], \
        speaker_activities=[speaker.speaker_id for speaker in speaker_activities], \
        minDate=datetime.strptime(event[0].start_date,'%d %b %Y, %a').strftime("%Y,%m,%d"), \
        maxDate=datetime.strptime(event[0].end_date,'%d %b %Y, %a').strftime("%Y,%m,%d"), \
        error=None)


@bp.route('/activity/<string:activity_external_id>', methods=['POST'])
@allowed_roles(['admin', 'activities_admin'])
def update_activity(activity_external_id):
    activity = ActivitiesFinder.get_from_external_id(activity_external_id)
    company_activities = ActivitiesFinder.get_company_activities_from_activity_id(activity_external_id)
    speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(activity_external_id)

    if activity is None:
        return APIErrorValue('Couldnt find activity').json(500)

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

    activity_type_external_id = request.form.get('type')
    activity_type = ActivityTypesFinder.get_from_external_id(uuid.UUID(activity_type_external_id))

    updated_activity = ActivitiesHandler.update_activity(
        activity=activity,
        activity_type=activity_type,
        name=name,
        description=description,
        location=location,
        day=day,
        time=time,
        registration_link=registration_link,
        registration_open=registration_open
    )

    if company_activities:
        for company_activity in company_activities:
            ActivitiesHandler.delete_company_activities(company_activity)

    if speaker_activities:
        for speaker_activity in speaker_activities:
            ActivitiesHandler.delete_speaker_activities(speaker_activity)

    # extract company names and speaker names from parameters
    companies = request.form.getlist('company')
    speakers = request.form.getlist('speaker')

    # if company names where provided
    if companies:
        for name in companies:
            company = CompaniesFinder.get_from_name(name)
            if company is None:
                return APIErrorValue('Couldnt find company').json(500)

            company_activity = ActivitiesHandler.add_company_activity(company, activity)
            if company_activity is None:
                return APIErrorValue('Failed to create company activity').json(500)

    if speakers:
        for name in speakers:
            speaker = SpeakersFinder.get_from_name(name)
            if speaker is None:
                return APIErrorValue('Couldnt find speaker').json(500)

            speaker_activity = ActivitiesHandler.add_speaker_activity(speaker, activity)
            if speaker_activity is None:
                return APIErrorValue('Failed to create speaker activity').json(500)
                
    if updated_activity is None:
        event = EventsFinder.get_from_parameters({"default": True})
    
        if event is None or len(event) == 0:
            error = 'No default event found! Please set a default event in the menu "Events"'
            return render_template('admin/activities/activities_dashboard.html', event=None, error=error, role=current_user.role.name)
        
        activity_types = event[0].activity_types

        return render_template('admin/activities/update_activity.html', \
            activity=activity, \
            types=activity_types, \
            companies=CompaniesFinder.get_all(), \
            speakers=SpeakersFinder.get_all(), \
            minDate=datetime.strptime(event[0].start_date,'%d %b %Y, %a').strftime("%Y,%m,%d"), \
            maxDate=datetime.strptime(event[0].end_date,'%d %b %Y, %a').strftime("%Y,%m,%d"), \
            error="Failed to update activity!")

    return redirect(url_for('admin_api.activities_dashboard'))


@bp.route('/activity/<string:activity_external_id>/delete', methods=['GET'])
@allowed_roles(['admin', 'activities_admin'])
def delete_activity(activity_external_id):
    activity = ActivitiesFinder.get_from_external_id(activity_external_id)
    company_activities = ActivitiesFinder.get_company_activities_from_activity_id(activity_external_id)
    speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(activity_external_id)

    if activity is None:
        return APIErrorValue('Couldnt find activity').json(500)
        
    if company_activities:
        for company_activity in company_activities:
            ActivitiesHandler.delete_company_activities(company_activity)

    if speaker_activities:
        for speaker_activity in speaker_activities:
            ActivitiesHandler.delete_speaker_activities(speaker_activity)

    if ActivitiesHandler.delete_activity(activity):
        return redirect(url_for('admin_api.activities_dashboard'))

    else:
        return render_template('admin/activities/update_activity.html', activity=activity, error="Failed to delete activity!")
