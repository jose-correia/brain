from .. import bp
from flask import render_template, current_app, request, redirect, url_for
from jeec_brain.handlers.events_handler import EventsHandler
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.apps.auth.wrappers import allowed_roles
from jeec_brain.services.files.delete_image_service import DeleteImageService
from flask_login import current_user
from datetime import datetime

# Events routes
@bp.route('/events', methods=['GET'])
@allowed_roles(['admin'])
def events_dashboard():
    search_parameters = request.args
    name = request.args.get('name')

    # handle search bar requests
    if name is not None:
        search = name
        events_list = EventsFinder.search_by_name(name)
    
    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = 'search name'

        events_list = EventsFinder.get_from_parameters(search_parameters)

    # request endpoint with no parameters should return all events
    else:
        search = None
        events_list = EventsFinder.get_all()
    
    if events_list is None or len(events_list) == 0:
        error = 'No results found'
        return render_template('admin/events/events_dashboard.html', events=None, error=error, search=search, role=current_user.role.name)

    now = datetime.utcnow()
    for event in events_list:
        if event.cvs_access_end:
            try:
                cvs_access_end = datetime.strptime(event.cvs_access_end, '%d %b %Y, %a')
            except:
                break
            event.cvs_purgeable = (now > cvs_access_end)
        else:
            event.cvs_purgeable = False

    return render_template('admin/events/events_dashboard.html', events=events_list, error=None, search=search, role=current_user.role.name)


@bp.route('/events', methods=['POST'])
@allowed_roles(['admin'])
def search_event():
    name = request.form.get('name')
    events_list = EventsFinder.search_by_name(name)

    if len(events_list) == 0:
        error = 'No results found'
        return render_template('admin/events/events_dashboard.html', events=None, error=error, search=name, role=current_user.role.name)

    return render_template('admin/events/events_dashboard.html', events=events_list, error=None, search=name, role=current_user.role.name)


@bp.route('/new-event', methods=['GET'])
@allowed_roles(['admin'])
def add_event_dashboard():
    return render_template('admin/events/add_event.html', error=None)


@bp.route('/new-event', methods=['POST'])
@allowed_roles(['admin'])
def create_event():
    name = request.form.get('name')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    cvs_submission_start = request.form.get('cvs_submission_start')
    cvs_submission_end = request.form.get('cvs_submission_end')
    cvs_access_start = request.form.get('cvs_access_start')
    cvs_access_end = request.form.get('cvs_access_end')
    email = request.form.get('email')
    location = request.form.get('location')
    default = request.form.get('default')
    facebook_event_link = request.form.get('facebook_event_link')
    facebook_link = request.form.get('facebook_link')
    youtube_link = request.form.get('youtube_link')
    instagram_link = request.form.get('instagram_link')
    show_schedule = request.form.get('show_schedule')
    show_registrations = request.form.get('show_registrations')

    if default == 'True':
        default = True
    else:
        default = False

    if show_schedule == 'True':
        show_schedule = True
    else:
        show_schedule = False

    if show_registrations == 'True':
        show_registrations = True
    else:
        show_registrations = False

    event = EventsHandler.create_event(
            name=name,
            start_date=start_date,
            end_date=end_date,
            default=default,
            email=email,
            location=location,
            facebook_link=facebook_link,
            facebook_event_link=facebook_event_link,
            youtube_link=youtube_link,
            instagram_link=instagram_link,
            show_schedule=show_schedule,
            show_registrations=show_registrations,
            cvs_submission_start=cvs_submission_start,
            cvs_submission_end=cvs_submission_end,
            cvs_access_start=cvs_access_start,
            cvs_access_end=cvs_access_end
        )

    if event is None:
        return render_template('admin/events/add_event.html', error="Failed to create event!")
    
    # there can only be one default
    if default:
        default_events = EventsFinder.get_from_parameters({"default": True})
        for default_event in default_events:
            if default_event is not event:
                EventsHandler.update_event(event=default_event, default=False)

    if request.files:
        image_file = request.files.get('event_image', None) 
        mobile_image_file = request.files.get('event_mobile_image', None)
        blueprint_file = request.files.get('event_blueprint', None)
        schedule_file = request.files.get('event_schedule', None)

        if image_file:
            result, msg = EventsHandler.upload_image(image_file, str(event.external_id))

            if result == False:
                EventsHandler.delete_event(event)
                return render_template('admin/events/add_event.html', error=msg)

        if mobile_image_file:
            image_name = f'{event.external_id}_mobile'
            result, msg = EventsHandler.upload_image(mobile_image_file, image_name)

            if result == False:
                EventsHandler.delete_event(event)
                return render_template('admin/events/add_event.html', error=msg)

        if blueprint_file:
            image_name = f'{event.external_id}_blueprint'
            result, msg = EventsHandler.upload_image(blueprint_file, image_name)

            if result == False:
                EventsHandler.delete_event(event)
                return render_template('admin/events/add_event.html', error=msg)

        if schedule_file:
            image_name = f'{event.external_id}_schedule'
            result, msg = EventsHandler.upload_image(blueprint_file, image_name)

            if result == False:
                EventsHandler.delete_event(event)
                return render_template('admin/events/add_event.html', error=msg)

    return redirect(url_for('admin_api.events_dashboard'))


@bp.route('/events/<string:event_external_id>', methods=['GET'])
@allowed_roles(['admin'])
def get_event(event_external_id):
    event = EventsFinder.get_from_external_id(event_external_id)

    if event is None:
        return render_template(url_for('admin_api.add_event_dashboard'))

    logo = EventsHandler.find_image(image_name=str(event.external_id))
    mobile_image_name = f'{event.external_id}_mobile'
    logo_mobile = EventsHandler.find_image(image_name=mobile_image_name)
    schedule_name = f'{event.external_id}_schedule'
    schedule = EventsHandler.find_image(image_name=schedule_name)
    blueprint_name = f'{event.external_id}_blueprint'
    blueprint = EventsHandler.find_image(image_name=blueprint_name)

    return render_template('admin/events/update_event.html', event=event, logo=logo, logo_mobile=logo_mobile, schedule=schedule, blueprint=blueprint, error=None)

@bp.route('/events/<string:event_external_id>', methods=['POST'])
@allowed_roles(['admin'])
def update_event(event_external_id):
    event = EventsFinder.get_from_external_id(event_external_id)
    if event is None:
        return APIErrorValue('Couldnt find event').json(500)

    name = request.form.get('name')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    cvs_submission_start = request.form.get('cvs_submission_start')
    cvs_submission_end = request.form.get('cvs_submission_end')
    cvs_access_start = request.form.get('cvs_access_start')
    cvs_access_end = request.form.get('cvs_access_end')
    default = request.form.get('default')
    email = request.form.get('email')
    location = request.form.get('location')
    facebook_event_link = request.form.get('facebook_event_link')
    facebook_link = request.form.get('facebook_link')
    youtube_link = request.form.get('youtube_link')
    instagram_link = request.form.get('instagram_link')
    show_schedule = request.form.get('show_schedule')
    show_registrations = request.form.get('show_registrations')

    if default == 'True':
        default = True
    else:
        default = False

    if show_schedule == 'True':
        show_schedule = True
    else:
        show_schedule = False

    if show_registrations == 'True':
        show_registrations = True
    else:
        show_registrations = False

    updated_event = EventsHandler.update_event(
        event=event,
        name=name,
        start_date=start_date,
        end_date=end_date,
        default=default,
        email=email,
        location=location,
        facebook_link=facebook_link,
        facebook_event_link=facebook_event_link,
        youtube_link=youtube_link,
        instagram_link=instagram_link,
        show_schedule=show_schedule,
        show_registrations=show_registrations,
        cvs_submission_start=cvs_submission_start,
        cvs_submission_end=cvs_submission_end,
        cvs_access_start=cvs_access_start,
        cvs_access_end=cvs_access_end
    )

    logo = EventsHandler.find_image(image_name=str(event.external_id))
    mobile_image_name = f'{event.external_id}_mobile'
    logo_mobile = EventsHandler.find_image(image_name=mobile_image_name)
    schedule_name = f'{event.external_id}_schedule'
    schedule = EventsHandler.find_image(image_name=schedule_name)
    blueprint_name = f'{event.external_id}_blueprint'
    blueprint = EventsHandler.find_image(image_name=blueprint_name)

    if updated_event is None:
        return render_template('admin/events/update_event.html', event=event, logo=logo, logo_mobile=logo_mobile, schedule=schedule, blueprint=blueprint, error=msg)

    # there can only be one default
    if default:
        default_events = EventsFinder.get_from_parameters({"default": True})
        for default_event in default_events:
            if default_event is not updated_event:
                EventsHandler.update_event(event=default_event, default=False)
    
    current_app.logger.error(request.files)

    if request.files:
        image_file = request.files.get('event_image', None) 
        mobile_image_file = request.files.get('event_mobile_image', None)
        blueprint_file = request.files.get('event_blueprint', None)
        schedule_file = request.files.get('event_schedule', None)

        if image_file:
            result, msg = EventsHandler.upload_image(image_file, str(updated_event.external_id))
            if result == False:
                return render_template('admin/events/update_event.html', event=event, logo=logo, logo_mobile=logo_mobile, schedule=schedule, blueprint=blueprint, error=msg)

        if mobile_image_file:
            image_name = f'{updated_event.external_id}_mobile'
            result, msg = EventsHandler.upload_image(mobile_image_file, image_name)
            if result == False:
                return render_template('admin/events/update_event.html', event=event, logo=logo, logo_mobile=logo_mobile, schedule=schedule, blueprint=blueprint, error=msg)

        if blueprint_file:
            image_name = f'{updated_event.external_id}_blueprint'
            result, msg = EventsHandler.upload_image(blueprint_file, image_name)
            if result == False:
                return render_template('admin/events/update_event.html', event=event, logo=logo, logo_mobile=logo_mobile, schedule=schedule, blueprint=blueprint, error=msg)

        if schedule_file:
            image_name = f'{updated_event.external_id}_schedule'
            result, msg = EventsHandler.upload_image(schedule_file, image_name)
            if result == False:
                return render_template('admin/events/update_event.html', event=event, logo=logo, logo_mobile=logo_mobile, schedule=schedule, blueprint=blueprint, error=msg)

    return redirect(url_for('admin_api.events_dashboard'))

@bp.route('/events/<string:event_external_id>/purge_cvs', methods=['POST'])
@allowed_roles(['admin'])
def purge_cvs(event_external_id):
    event = EventsFinder.get_from_external_id(event_external_id)
    if event is None:
        return APIErrorValue('Couldnt find event').json(500)

    #
    #
    #