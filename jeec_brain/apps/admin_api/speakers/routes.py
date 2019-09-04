from .. import bp
from flask import render_template, request, redirect, url_for
from jeec_brain.finders.speakers_finder import SpeakersFinder
from jeec_brain.handlers.speakers_handler import SpeakersHandler
from jeec_brain.apps.auth.wrappers import require_admin_login
from jeec_brain.values.api_error_value import APIErrorValue


@bp.route('/speakers', methods=['GET'])
@require_admin_login
def speakers_dashboard():
    speakers_list = SpeakersFinder.get_all()

    return render_template('admin/speakers/speakers_dashboard.html', speakers=speakers_list)


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

    return redirect(url_for('admin_api.speakers_dashboard'))


@bp.route('/speaker/<string:speaker_external_id>', methods=['GET'])
@require_admin_login
def get_speaker(speaker_external_id):
    speaker = SpeakersFinder.get_from_external_id(speaker_external_id)

    return render_template('admin/speakers/update_speaker.html', speaker=speaker)


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
        return render_template('admin/speakers/update_speaker.html', speaker=speaker, error="Failed to update speaker!")

    return redirect(url_for('admin_api.speakers_dashboard'))


@bp.route('/speaker/<string:speaker_external_id>/delete', methods=['GET'])
@require_admin_login
def delete_speaker(speaker_external_id):
    speaker = SpeakersFinder.get_from_external_id(speaker_external_id)

    if speaker is None:
        return APIErrorValue('Couldnt find speaker').json(500)
        
    if SpeakersHandler.delete_speaker(speaker):
        return redirect(url_for('admin_api.speakers_dashboard'))

    else:
        return render_template('admin/speakers/update_speaker.html', speaker=speaker, error="Failed to delete speaker!")

