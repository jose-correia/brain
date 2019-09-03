from .. import bp
from flask import render_template
from jeec_brain.finders.colaborator_finder import ColaboratorFinder
from jeec_brain.apps.auth.wrappers import require_admin_login


# Team routes
@bp.route('/team', methods=['GET'])
@require_admin_login
def team_dashboard():
    colaborators_list = ColaboratorFinder.get_all()

    return render_template('admin/team_dashboard.html', colaborators=colaborators_list)
