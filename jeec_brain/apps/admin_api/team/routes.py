from .. import bp
from flask import render_template, request, redirect, url_for
from jeec_brain.finders.teams_finder import TeamsFinder
from jeec_brain.finders.colaborators_finder import ColaboratorsFinder
from jeec_brain.handlers.teams_handler import TeamsHandler
from jeec_brain.apps.auth.wrappers import require_admin_login
from jeec_brain.values.api_error_value import APIErrorValue


# Team management
@bp.route('/teams', methods=['GET'])
@require_admin_login
def teams_dashboard():
    teams_list = TeamsFinder.get_all()

    if len(teams_list) == 0:
        error = 'No results found'
        return render_template('admin/teams/teams_dashboard.html', teams=None, error=error, search=None)

    return render_template('admin/teams/teams_dashboard.html', teams=teams_list, error=None, search=None)


@bp.route('/teams', methods=['POST'])
@require_admin_login
def search_team():
    name = request.form.get('name')
    teams_list = TeamsFinder.search_by_name(name)

    if len(teams_list) == 0:
        error = 'No results found'
        return render_template('admin/teams/teams_dashboard.html', teams=None, error=error, search=name)

    return render_template('admin/teams/teams_dashboard.html', teams=teams_list, error=None, search=name)


@bp.route('/new-team', methods=['GET'])
@require_admin_login
def add_team_dashboard():
    return render_template('admin/teams/add_team.html')


@bp.route('/new-team', methods=['POST'])
@require_admin_login
def create_team():
    name = request.form.get('name')
    description = request.form.get('description')

    team = TeamsHandler.create_team(
        name=name,
        description=description
    )
    
    if team is None:
        return render_template('admin/teams/add_team.html', error="Failed to create team!")

    return redirect(url_for('admin_api.teams_dashboard'))


@bp.route('/team/<string:team_external_id>', methods=['GET'])
@require_admin_login
def get_team(team_external_id):
    team = TeamsFinder.get_from_external_id(team_external_id)

    return render_template('admin/teams/update_team.html', team=team)


@bp.route('/team/<string:team_external_id>', methods=['POST'])
@require_admin_login
def update_team(team_external_id):
    team = TeamsFinder.get_from_external_id(team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    name = request.form.get('name')
    description = request.form.get('description')

    updated_team = TeamsHandler.update_team(
        team=team,
        name=name,
        description=description
    )
    
    if updated_team is None:
        return render_template('admin/teams/update_team.html', team=team, error="Failed to update team!")

    return redirect(url_for('admin_api.teams_dashboard'))


@bp.route('/team/<string:team_external_id>/delete', methods=['GET'])
@require_admin_login
def delete_team(team_external_id):
    team = TeamsFinder.get_from_external_id(team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)
        
    if TeamsHandler.delete_team(team):
        return redirect(url_for('admin_api.teams_dashboard'))

    else:
        return render_template('admin/teams/update_team.html', team=team, error="Failed to delete team!")


# Members management
@bp.route('/team/<string:team_external_id>/members', methods=['GET'])
@require_admin_login
def team_members_dashboard(team_external_id):
    team = TeamsFinder.get_from_external_id(team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    if len(team.members.all()) == 0:
        error = 'No results found'
        return render_template('admin/teams/team_members_dashboard.html', team=team, members=None, error=error, search=None)

    return render_template('admin/teams/team_members_dashboard.html', team=team, members=team.members, error=None, search=None)


@bp.route('/team/<string:team_external_id>/members', methods=['POST'])
@require_admin_login
def search_team_members(team_external_id):
    team = TeamsFinder.get_from_external_id(team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    name = request.form.get('name')
    members_list = ColaboratorsFinder.search_by_name(name)

    if len(members_list) == 0:
        error = 'No results found'
        return render_template('admin/teams/team_members_dashboard.html', team=team, members=None, error=error, search=name)

    return render_template('admin/teams/team_members_dashboard.html', team=team, members=members_list, error=None, search=name)


@bp.route('/team/<string:team_external_id>/new-member', methods=['GET'])
@require_admin_login
def add_team_member_dashboard(team_external_id):
    team = TeamsFinder.get_from_external_id(team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    return render_template('admin/teams/add_team_member.html', team=team)


@bp.route('/team/<string:team_external_id>/new-member', methods=['POST'])
@require_admin_login
def create_team_member(team_external_id):
    team = TeamsFinder.get_from_external_id(team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    name = request.form.get('name')
    ist_id = request.form.get('ist_id')
    email = request.form.get('email')
    linkedin_url = request.form.get('linkedin_url')

    member = TeamsHandler.create_team_member(
        team=team,
        name=name,
        ist_id=ist_id,
        email=email,
        linkedin_url=linkedin_url
    )
    
    if member is None:
        return render_template('admin/teams/add_team_member.html', team=team, error="Failed to create team member!")

    if 'file' in request.files:
        file = request.files['file']
        result, msg = TeamsHandler.upload_member_image(file, name)

        if result == False:
            TeamsHandler.delete_team_member(member)
            return render_template('admin/teams/add_team_member.html', team=team, error=msg)

    return redirect(url_for('admin_api.team_members_dashboard', team_external_id=team_external_id))


@bp.route('/team/<string:team_external_id>/members/<string:member_external_id>', methods=['GET'])
@require_admin_login
def get_team_member(team_external_id, member_external_id):
    team = TeamsFinder.get_from_external_id(team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    member = ColaboratorsFinder.get_from_external_id(member_external_id)

    if member is None:
        return APIErrorValue('Couldnt find team member').json(500)

    image_path = TeamsHandler.find_member_image(member.name)

    return render_template('admin/teams/update_team_member.html', member=member, image=image_path, error=None)


@bp.route('/team/<string:team_external_id>/members/<string:member_external_id>', methods=['POST'])
@require_admin_login
def update_team_member(team_external_id, member_external_id):
    team = TeamsFinder.get_from_external_id(team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    member = ColaboratorsFinder.get_from_external_id(member_external_id)

    if member is None:
        return APIErrorValue('Couldnt find team member').json(500)

    name = request.form.get('name')
    ist_id = request.form.get('ist_id')
    email = request.form.get('email')
    linkedin_url = request.form.get('linkedin_url')

    updated_member = TeamsHandler.update_team_member(
        member=member,
        name=name,
        ist_id=ist_id,
        email=email,
        linkedin_url=linkedin_url
    )

    image_path = TeamsHandler.find_member_image(name)
    
    if updated_member is None:
        return render_template('admin/teams/update_team_member.html', member=member, image=image_path, error="Failed to update team member!")

    if 'file' in request.files:
        file = request.files['file']

        result, msg = TeamsHandler.upload_member_image(file, name)

        if result == False:
            return render_template('admin/teams/update_team_member.html', member=update_team_member, image=image_path, error=msg)

    return redirect(url_for('admin_api.team_members_dashboard', team_external_id=team_external_id))


@bp.route('/team/<string:team_external_id>/members/<string:member_external_id>/delete', methods=['GET'])
@require_admin_login
def delete_team_member(team_external_id, member_external_id):
    team = TeamsFinder.get_from_external_id(team_external_id)

    if team is None:
        return APIErrorValue('Couldnt find team').json(500)

    member = ColaboratorsFinder.get_from_external_id(member_external_id)

    if member is None:
        return APIErrorValue('Couldnt find team member').json(500)
    
    name = member.name

    if TeamsHandler.delete_team_member(member):
        TeamsHandler.delete_member_image(name)
        return redirect(url_for('admin_api.team_members_dashboard', team_external_id=team_external_id))

    else:
        image_path = TeamsHandler.find_member_image(name)
        return render_template('admin/teams/update_team_member.html', member=member, image=image_path, error="Failed to delete team member!")
