from .. import bp
from flask import render_template, current_app
from jeec_brain.finders.activity_finder import ActivityFinder
from jeec_brain.apps.auth.wrappers import require_admin_login


# Activities routes
@bp.route('/activities', methods=['GET'])
@require_admin_login
def activities_dashboard():
    activities_list = current_app.config['ACTIVITIES']

    return render_template('admin/activities_dashboard.html', colaborators=activities_list)
