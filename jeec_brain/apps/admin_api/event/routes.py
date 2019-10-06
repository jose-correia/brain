from .. import bp
from flask import render_template, current_app, request, redirect, url_for
from jeec_brain.handlers.event_handler import EventHandler
from jeec_brain.finders.event_finder import EventFinder
from jeec_brain.apps.auth.wrappers import allowed_roles
from jeec_brain.models.enums.roles_enum import RolesEnum
from flask_login import current_user


@bp.route('/new-event', methods=['GET'])
@allowed_roles(['admin')
def add_event_dashboard():
    return render_template('admin/event/add_event.html', \
        error=None)


@bp.route('/new-event', methods=['POST'])
@allowed_roles(['admin'])
def create_event():
    # extract form parameters
    name = request.form.get('name')
    date = request.form.get('date')
    email = request.form.get('email')
    address = request.form.get('address')
    facebook_link = request.form.get('facebook_link')
    youtube_link = request.form.get('youtube_link')
    instagram_link = request.form.get('instagram_link')

    # create new user
    event = EventHandler.create_event(
            name=name,
            date=date,
            email=email,
            address=address,
            facebook_link=facebook_link,
            youtube_link=youtube_link,
            instagram_link=instagram_link
        )

    if event is None:
        return render_template('admin/event/add_event.html', \
            error="Failed to create event!")

    return redirect(url_for('admin_api.get_event'))


@bp.route('/event', methods=['GET'])
@allowed_roles(['admin')
def get_event():
    event = EventsFinder.get_event()

    if event is None:
        return render_template(url_for('admin_api.add_event_dashboard'))

    logo = EventHandler.find_logo()
    logo_mobile = EventHandler.find_logo_mobile()
    return render_template('admin/event/update_event.html', event=event, image=image_path, error=None)


@bp.route('/event/<string:event_external_id>', methods=['POST'])
@allowed_roles(['admin'])
def update_event(event_external_id):

    company = EventFinder.get_event()

    if company is None:
        return APIErrorValue('Couldnt find company').json(500)

    name = request.form.get('name')
    date = request.form.get('date')
    email = request.form.get('email')
    address = request.form.get('address')
    facebook_link = request.form.get('facebook_link')
    youtube_link = request.form.get('youtube_link')
    instagram_link = request.form.get('instagram_link')

    image_path = CompaniesHandler.find_image(name)

    updated_event = EventHandler.update_event(
        name=name,
        date=date,
        email=email,
        address=address,
        facebook_link=facebook_link,
        youtube_link=youtube_link,
        instagram_link=instagram_link
    )
    
    if updated_event is None:
        return render_template('admin/event/update_event.html', event=event, image=image_path, error="Failed to update company!")

    if 'file' in request.files:
        file = request.files['file']

        result, msg = CompaniesHandler.upload_image(file, name)

        if result == False:
            return render_template('admin/companies/update_company.html', company=updated_company, image=image_path, error=msg)

    return redirect(url_for('admin_api.companies_dashboard'))
