from .. import bp
from flask import render_template
from jeec_brain.finders.teams_finder import TeamsFinder
from jeec_brain.handlers.teams_handler import TeamsHandler
from jeec_brain.apps.auth.wrappers import require_admin_login


# Team routes
@bp.route('/team', methods=['GET'])
@require_admin_login
def team_dashboard():
    colaborators_list = ColaboratorFinder.get_all()

    return render_template('admin/team_dashboard.html', colaborators=colaborators_list)
