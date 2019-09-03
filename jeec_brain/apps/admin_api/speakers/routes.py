from .. import bp
from flask import render_template
from jeec_brain.finders.speakers_finder import SpeakersFinder
from jeec_brain.handlers.speakers_handler import SpeakersHandler
from jeec_brain.apps.auth.wrappers import require_admin_login


# Speakers routes
@bp.route('/speakers', methods=['GET'])
@require_admin_login
def speakers_dashboard():
    speakers_list = SpeakerFinder.get_all()

    return render_template('admin/speakers_dashboard.html', speakers=speakers_list)
