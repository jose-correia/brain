from .. import bp
from flask import render_template, request, redirect, url_for, current_app
from jeec_brain.finders.speakers_finder import SpeakersFinder
from jeec_brain.handlers.speakers_handler import SpeakersHandler
from jeec_brain.apps.auth.wrappers import require_admin_login
from jeec_brain.values.api_error_value import APIErrorValue


@bp.route('/speakers', methods=['GET'])
@require_admin_login
def speakers_dashboard():
    speakers_list = SpeakersFinder.get_all()

    if len(speakers_list) == 0:
        error = 'No results found'
        return render_template('admin/speakers/speakers_dashboard.html', speakers=None, error=error, search=None)

    return render_template('admin/speakers/speakers_dashboard.html', speakers=speakers_list, error=None, search=None)


@bp.route('/speakers', methods=['POST'])
@require_admin_login
def search_speaker():
    name = request.form.get('name')
    speakers_list = SpeakersFinder.search_by_name(name)

    if len(speakers_list) == 0:
        error = 'No results found'
        return render_template('admin/speakers/speakers_dashboard.html', speakers=speakers_list, error=error, search=name)

    return render_template('admin/speakers/speakers_dashboard.html', speakers=speakers_list, error=None, search=name)


@bp.route('/new-speaker', methods=['GET'])
@require_admin_login
def add_speaker_dashboard():
    return render_template('admin/speakers/add_speaker.html')


@bp.route('/new-speaker', methods=['POST'])
@require_admin_login
def create_speaker():
    name = request.form.get('name')
    company = request.form.get('company')
    position = request.form.get('position')
    country = request.form.get('country')
    bio = request.form.get('bio')
    linkedin_url = request.form.get('linkedin_url')

    speaker = SpeakersHandler.create_speaker(
        name=name,
        company=company,
        position=position,
        country=country,
        bio=bio,
        linkedin_url=linkedin_url
    )

    if speaker is None:
        return render_template('admin/speakers/add_speaker.html', error="Failed to create speaker!")

    if 'file' in request.files:
        file = request.files['file']
        result, msg = SpeakersHandler.upload_image(file, name)

        if result == False:
            SpeakersHandler.delete_speaker(speaker)
            return render_template('admin/speakers/add_speaker.html', error=msg)

    return redirect(url_for('admin_api.speakers_dashboard'))


@bp.route('/speaker/<string:speaker_external_id>', methods=['GET'])
@require_admin_login
def get_speaker(speaker_external_id):
    speaker = SpeakersFinder.get_from_external_id(speaker_external_id)

    image_path = SpeakersHandler.find_image(name)

    return render_template('admin/speakers/update_speaker.html', speaker=speaker, image=image_path, error=None)


@bp.route('/speaker/<string:speaker_external_id>', methods=['POST'])
@require_admin_login
def update_speaker(speaker_external_id):

    speaker = SpeakersFinder.get_from_external_id(speaker_external_id)

    if speaker is None:
        return APIErrorValue('Couldnt find speaker').json(500)

    name = request.form.get('name')
    company = request.form.get('company')
    position = request.form.get('position')
    country = request.form.get('country')
    bio = request.form.get('bio')
    linkedin_url = request.form.get('linkedin_url')

    image_path = SpeakersHandler.find_image(name)

    updated_speaker = SpeakersHandler.update_speaker(
        speaker=speaker,
        name=name,
        company=company,
        position=position,
        country=country,
        bio=bio,
        linkedin_url=linkedin_url
    )
    
    if updated_speaker is None:
        return render_template('admin/speakers/update_speaker.html', speaker=speaker, image=image_path, error="Failed to update speaker!")

    if 'file' in request.files:
        file = request.files['file']

        result, msg = SpeakersHandler.upload_image(file, name)

        if result == False:
            return render_template('admin/speakers/update_speaker.html', speaker=updated_speaker, image=image_path, error=msg)

    return redirect(url_for('admin_api.speakers_dashboard'))


@bp.route('/speaker/<string:speaker_external_id>/delete', methods=['GET'])
@require_admin_login
def delete_speaker(speaker_external_id):
    speaker = SpeakersFinder.get_from_external_id(speaker_external_id)

    if speaker is None:
        return APIErrorValue('Couldnt find speaker').json(500)

    name = speaker.name
        
    if SpeakersHandler.delete_speaker(speaker):
        SpeakersHandler.delete_image(name)
        return redirect(url_for('admin_api.speakers_dashboard'))

    else:
        image_path = SpeakersHandler.find_image(name)
        return render_template('admin/speakers/update_speaker.html', speaker=speaker, image=image_path, error="Failed to delete speaker!")

