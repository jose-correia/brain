from .. import bp
from flask import render_template, request, redirect, url_for, make_response, jsonify, send_file
from jeec_brain.finders.teams_finder import TeamsFinder
from jeec_brain.finders.colaborators_finder import ColaboratorsFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.handlers.teams_handler import TeamsHandler
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.admin_api.team.schemas import *
from flask_login import current_user
from jeec_brain.services.files.rename_image_service import RenameImageService
from PIL import Image

import json

from jeec_brain.apps.auth.wrappers import requires_client_auth


# Team management
@bp.get("/teams")
@allow_all_roles
def teams_dashboard():
    default_event = EventsFinder.get_default_event()
    events = EventsFinder.get_all()
    teams_list = TeamsFinder.get_from_parameters({"event_id": default_event.id})

    if len(teams_list) == 0:
        error = "No results found"
        return render_template(
            "admin/teams/teams_dashboard.html",
            teams=None,
            events=events,
            selected_event=default_event.id,
            error=error,
            search=None,
            role=current_user.role.name,
        )

    return render_template(
        "admin/teams/teams_dashboard.html",
        teams=teams_list,
        events=events,
        selected_event=default_event.id,
        error=None,
        search=None,
        role=current_user.role.name,
    )


@bp.post("/teams")
@allow_all_roles
def search_team():
    name = request.form.get("name", None)
    event_id = request.form.get("event", None)
    events = EventsFinder.get_all()
    search_parameters = {}

    if name is not None:
        search_parameters["name"] = name
    if event_id is not None:
        search_parameters["event_id"] = event_id

    teams_list = TeamsFinder.get_from_parameters(search_parameters)

    if len(teams_list) == 0:
        error = "No results found"
        return render_template(
            "admin/teams/teams_dashboard.html",
            teams=None,
            events=events,
            selected_event=event_id,
            error=error,
            search=name,
            role=current_user.role.name,
        )

    return render_template(
        "admin/teams/teams_dashboard.html",
        teams=teams_list,
        events=events,
        selected_event=event_id,
        error=None,
        search=name,
        role=current_user.role.name,
    )


@bp.get("/new-team")
@allowed_roles(["admin", "teams_admin"])
def add_team_dashboard():
    events = EventsFinder.get_all()
    return render_template("admin/teams/add_team.html", events=events)


@bp.post("/new-team")
@allowed_roles(["admin", "teams_admin"])
def create_team():
    name = request.form.get("name")
    description = request.form.get("description")
    website_priority = request.form.get("website_priority")
    event_id = request.form.get("event")

    event = EventsFinder.get_from_id(event_id)
    if name in [team.name for team in event.teams]:
        return render_template(
            "admin/teams/add_team.html",
            error="Failed to create team! Team name already exists",
        )

    if not website_priority:
        website_priority = 0

    team = TeamsHandler.create_team(
        name=name,
        description=description,
        website_priority=website_priority,
        event_id=event_id,
    )

    if team is None:
        return render_template(
            "admin/teams/add_team.html", error="Failed to create team!"
        )

    return redirect(url_for("admin_api.teams_dashboard"))


@bp.get("/team/<string:team_external_id>")
@allowed_roles(["admin", "teams_admin"])
def get_team(path: TeamPath):
    team = TeamsFinder.get_from_external_id(path.team_external_id)
    events = EventsFinder.get_all()

    return render_template("admin/teams/update_team.html", team=team, events=events)


@bp.post("/team/<string:team_external_id>")
@allowed_roles(["admin", "teams_admin"])
def update_team(path: TeamPath):
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue("Couldnt find team").json(500)

    name = request.form.get("name")
    description = request.form.get("description")
    website_priority = request.form.get("website_priority")
    event_id = request.form.get("event")

    event = EventsFinder.get_from_id(event_id)
    if name in [team.name for team in event.teams]:
        return render_template(
            "admin/teams/add_team.html",
            error="Failed to update team! Team name already exists",
        )

    updated_team = TeamsHandler.update_team(
        team=team,
        name=name,
        description=description,
        website_priority=website_priority,
        event_id=event_id,
    )

    if updated_team is None:
        return render_template(
            "admin/teams/update_team.html", team=team, error="Failed to update team!"
        )

    return redirect(url_for("admin_api.teams_dashboard"))


@bp.get("/team/<string:team_external_id>/delete")
@allowed_roles(["admin", "teams_admin"])
def delete_team(path: TeamPath):
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue("Couldnt find team").json(500)

    if TeamsHandler.delete_team(team):
        return redirect(url_for("admin_api.teams_dashboard"))

    else:
        return render_template(
            "admin/teams/update_team.html", team=team, error="Failed to delete team!"
        )


# Members management
@bp.get("/team/<string:team_external_id>/members")
@allow_all_roles
def team_members_dashboard(path: TeamPath):
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue("Couldnt find team").json(500)

    if len(team.members.all()) == 0:
        error = "No results found"
        return render_template(
            "admin/teams/team_members_dashboard.html",
            team=team,
            members=None,
            error=error,
            search=None,
            role=current_user.role.name,
        )

    return render_template(
        "admin/teams/team_members_dashboard.html",
        team=team,
        members=team.members,
        error=None,
        search=None,
        role=current_user.role.name,
    )


@bp.post("/team/<string:team_external_id>/members")
@allow_all_roles
def search_team_members(path: TeamPath):
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue("Couldnt find team").json(500)

    name = request.form.get("name")
    members_list = ColaboratorsFinder.search_by_name(name)

    if len(members_list) == 0:
        error = "No results found"
        return render_template(
            "admin/teams/team_members_dashboard.html",
            team=team,
            members=None,
            error=error,
            search=name,
            role=current_user.role.name,
        )

    return render_template(
        "admin/teams/team_members_dashboard.html",
        team=team,
        members=members_list,
        error=None,
        search=name,
        role=current_user.role.name,
    )


@bp.get("/team/<string:team_external_id>/erase")
@allowed_roles(["admin", "teams_admin"])
def delete_all_team_members(path: TeamPath):
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue("Couldnt find team").json(500)

    members = ColaboratorsFinder.get_all_from_team(team)

    if not members:
        return APIErrorValue("Couldnt find team members").json(500)

    for member in members:
        TeamsHandler.delete_team_member(member)
    return redirect(
        url_for(
            "admin_api.team_members_dashboard", team_external_id=path.team_external_id
        )
    )


@bp.get("/team/<string:team_external_id>/new-member")
@allowed_roles(["admin", "teams_admin"])
def add_team_member_dashboard(path: TeamPath):
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue("Couldnt find team").json(500)

    return render_template("admin/teams/add_team_member.html", team=team)


@bp.post("/team/<string:team_external_id>/new-member")
@allowed_roles(["admin", "teams_admin"])
def create_team_member(path: TeamPath):
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue("Couldnt find team").json(500)

    name = request.form.get("name")
    ist_id = request.form.get("ist_id")
    email = request.form.get("email")
    linkedin_url = request.form.get("linkedin_url")

    if len(ColaboratorsFinder.get_from_event_and_name(team.event_id, name)) > 0:
        return render_template(
            "admin/teams/add_team_member.html",
            team=team,
            error="Failed to create team member! Colaborator already exists",
        )

    member = TeamsHandler.create_team_member(
        team=team, name=name, ist_id=ist_id, email=email, linkedin_url=linkedin_url
    )

    if member is None:
        return render_template(
            "admin/teams/add_team_member.html",
            team=team,
            error="Failed to create team member!",
        )

    if "file" in request.files:
        file = request.files["file"]
        if file.filename:
            result, msg = TeamsHandler.upload_member_image(file, name)

            if result == False:
                TeamsHandler.delete_team_member(member)
                return render_template(
                    "admin/teams/add_team_member.html", team=team, error=msg
                )

    return redirect(
        url_for(
            "admin_api.team_members_dashboard", team_external_id=path.team_external_id
        )
    )


@bp.get("/team/<string:team_external_id>/members/<string:member_external_id>")
@allowed_roles(["admin", "teams_admin"])
def get_team_member(path: TeamMemberPath):
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue("Couldnt find team").json(500)

    member = ColaboratorsFinder.get_from_external_id(path.member_external_id)

    if member is None:
        return APIErrorValue("Couldnt find team member").json(500)

    image_path = TeamsHandler.find_member_image(member.name)

    return render_template(
        "admin/teams/update_team_member.html",
        member=member,
        image=image_path,
        error=None,
    )


@bp.post("/team/<string:team_external_id>/members/<string:member_external_id>")
@allowed_roles(["admin", "teams_admin"])
def update_team_member(path: TeamMemberPath):
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue("Couldnt find team").json(500)

    member = ColaboratorsFinder.get_from_external_id(path.member_external_id)

    if member is None:
        return APIErrorValue("Couldnt find team member").json(500)

    name = request.form.get("name")
    ist_id = request.form.get("ist_id")
    email = request.form.get("email")
    linkedin_url = request.form.get("linkedin_url")

    old_member_name = member.name

    if len(ColaboratorsFinder.get_from_event_and_name(team.event_id, name)) > 1:
        return render_template(
            "admin/teams/add_team_member.html",
            team=team,
            error="Failed to create team member! Colaborator already exists",
        )

    updated_member = TeamsHandler.update_team_member(
        member=member, name=name, ist_id=ist_id, email=email, linkedin_url=linkedin_url
    )

    image_path = TeamsHandler.find_member_image(name)

    if updated_member is None:
        return render_template(
            "admin/teams/update_team_member.html",
            member=member,
            image=image_path,
            error="Failed to update team member!",
        )

    if old_member_name != name:
        RenameImageService("static/members", old_member_name, name).call()

    if "file" in request.files:
        file = request.files["file"]
        if file.filename:
            result, msg = TeamsHandler.upload_member_image(file, name)

            if result == False:
                return render_template(
                    "admin/teams/update_team_member.html",
                    member=updated_member,
                    image=image_path,
                    error=msg,
                )

    return redirect(
        url_for(
            "admin_api.team_members_dashboard", team_external_id=path.team_external_id
        )
    )


@bp.get("/team/<string:team_external_id>/members/<string:member_external_id>/delete")
@allowed_roles(["admin", "teams_admin"])
def delete_team_member(path: TeamMemberPath):
    team = TeamsFinder.get_from_external_id(path.team_external_id)

    if team is None:
        return APIErrorValue("Couldnt find team").json(500)

    member = ColaboratorsFinder.get_from_external_id(path.member_external_id)

    if member is None:
        return APIErrorValue("Couldnt find team member").json(500)

    name = member.name

    if TeamsHandler.delete_team_member(member):
        return redirect(
            url_for(
                "admin_api.team_members_dashboard",
                team_external_id=path.team_external_id,
            )
        )

    else:
        image_path = TeamsHandler.find_member_image(name)
        return render_template(
            "admin/teams/update_team_member.html",
            member=member,
            image=image_path,
            error="Failed to delete team member!",
        )

 #versão vue 
 
# Team management
@bp.get("/teams-vue")
@requires_client_auth
def teams_dashboard_vue():

    events = EventsFinder.get_all()
    teams_list = TeamsFinder.get_all()
    
    eventts = []
    for event in events:
        event_vue = {
            "name": event.name,
            "external_id": event.external_id,
            "id": event.id,
        }
        eventts.append(event_vue)
        
        
    teams_listt = []
    for team in teams_list:
        members = []
        for memberr in team.members:
            member_vue = {
                "name": memberr.name,
                "ist_id": memberr.ist_id,
                "email": memberr.email,
                "linkedin_url": memberr.linkedin_url,
            }
            members.append(member_vue)
            
        team_vue = {
            "name": team.name,
            "website_priority": team.website_priority,
            "event": team.event.name,
            "event_id": team.event.id,
            "id": team.id,
            "description": team.description,
            "members": members,
            "external_id": team.external_id,
        }
        teams_listt.append(team_vue)


    if len(teams_listt) == 0:
        response = make_response(
        jsonify({
            "teams": [],
            "error": 'No results found',
            "events": eventts,
            
        })
        )
        return response

    response = make_response(
    jsonify({
        "teams": teams_listt,
        "error": '',
        "events": eventts,
        
    })
    )
    return response


@bp.get("/new-team-vue")
@requires_client_auth
def add_team_dashboard_vue():
    
    events = EventsFinder.get_all()
    
    eventts = []
    for event in events:
        event_vue = {
            "name": event.name,
            "external_id": event.external_id,
            "id": event.id,
        }
        eventts.append(event_vue)
        
    response = make_response(
    jsonify({
        "events": eventts,
    })
    )
    return response

 

@bp.post("/new-team-vue")
@requires_client_auth
def create_team_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    name = response['name']
    description = response['description']
    website_priority = response['website_priority']
    event_id = response['event_id']
    

    event = EventsFinder.get_from_id(event_id)
    if name in [team.name for team in event.teams]:
        response = make_response(
        jsonify({
            "error": 'Failed to create team! Team name already exists',
        })
        )
        return response

    if not website_priority:
        website_priority = 0

    team = TeamsHandler.create_team(
        name=name,
        description=description,
        website_priority=website_priority,
        event_id=event_id,
    )

    if team is None:
        
        response = make_response(
        jsonify({
            "error": 'Failed to create team!',
        })
        )
        return response
    response = make_response(
    jsonify({
        "error": '',
    })
    )
    return response
 

@bp.post("/team/getteamup")
@requires_client_auth
def get_team_vue():
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    team = TeamsFinder.get_from_external_id(external_id)
    
    events = EventsFinder.get_all()
    
    eventts = []
    for event in events:
        event_vue = {
            "name": event.name,
            "external_id": event.external_id,
            "id": event.id,
        }
        eventts.append(event_vue)
        
    members = []
    for memberr in team.members:
        member_vue = {
            "name": memberr.name,
            "ist_id": memberr.ist_id,
            "email": memberr.email,
            "linkedin_url": memberr.linkedin_url,
        }
        members.append(member_vue)
            
    teamm = {
        "name": team.name,
        "website_priority": team.website_priority,
        "event": team.event.name,
        "event_id": team.event.id,
        "id": team.id,
        "description": team.description,
        "members": members,
    }
        
    response = make_response(
    jsonify({
        "events": eventts,
        "team": teamm,
        "error": '',
    })
    )
    return response


@bp.post("/team/updateteam")
@requires_client_auth
def update_team_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    team = TeamsFinder.get_from_external_id(external_id)
    name = response['name']
    description = response['description']
    website_priority = response['website_priority']
    event_id = response['event_id']
    

    if team is None:
        response = make_response(
        jsonify({
            "error": 'No team found',
        })
        )
        return response

    event = EventsFinder.get_from_id(event_id)

    updated_team = TeamsHandler.update_team(
        team=team,
        name=name,
        description=description,
        website_priority=website_priority,
        event_id=event_id,
    )

    if updated_team is None:
        response = make_response(
        jsonify({
            "error": 'Failed to update team!',
        })
        )
        return response
    
    response = make_response(
    jsonify({
        "error": '',
    })
    )
    return response


@bp.post("/team/delete")
@requires_client_auth
def delete_team_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    team = TeamsFinder.get_from_external_id(external_id)
    
    if team is None:
        response = make_response(
        jsonify({
            "error": 'Couldnt find team',
        })
        )
        return response
   
    if TeamsHandler.delete_team(team):
 
        response = make_response(
        jsonify({
            "error": '',
        })
        )
        return response

    else:
        response = make_response(
        jsonify({
            "error": 'Failed to delete team!',
        })
        )
        return response


# Members management
@bp.post("/team/members")
@requires_client_auth
def team_members_dashboard_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    team = TeamsFinder.get_from_external_id(external_id)
 
    members = []
    for memberr in team.members:
        member_vue = {
            "name": memberr.name,
            "ist_id": memberr.ist_id,
            "email": memberr.email,
            "linkedin_url": memberr.linkedin_url,
            "external_id": memberr.external_id
        }
        members.append(member_vue)
     
    teamm = {
        "name": team.name,
        "website_priority": team.website_priority,
        "event": team.event.name,
        "event_id": team.event.id,
        "id": team.id,
        "description": team.description,
        "members": members,
    }

    if team is None:
        
        response = make_response(
        jsonify({
            'error': 'Couldnt find team!',
            'team': [],
            'members': [],
        })
        )
        return response


    if len(team.members.all()) == 0:
        error = "No results found"
        response = make_response(
        jsonify({
            'error': error,
            'team': teamm,
            'members': [],
        })
        )
        return response

    response = make_response(
    jsonify({
        'error': '',
        'team': teamm,
        'members': members,
    })
    )
    return response

@bp.post("/team/erase")
@requires_client_auth
def delete_all_team_members_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    team = TeamsFinder.get_from_external_id(external_id)

    if team is None:
        response = make_response(
        jsonify({
            'error': 'Couldnt find team',
        })
        )
        return response

    members = ColaboratorsFinder.get_all_from_team(team)

    if not members:
        response = make_response(
        jsonify({
            'error': 'Couldnt find team members',
        })
        )
        return response

    for member in members:
        TeamsHandler.delete_team_member(member)
    response = make_response(
    jsonify({
        'error': '',
    })
    )
    return response

@bp.post("getimagespeaker")
@requires_client_auth
def getimagespeaker_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    member_external_id = response['member_external_id']
    member = ColaboratorsFinder.get_from_external_id(member_external_id)
    member_name = member.name
    
    fileUp = TeamsHandler.get_image_member(member_name)
    

    if not fileUp:
        return Response(response="Invalid zip file", status="200")
    
    filedown = Image.open(fileUp)
 
    return send_file(
        fileUp
    )
    
     
    
@bp.post("/team/members/create_url_error")
@requires_client_auth
def create_url_error_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    member_external_id = response['member_external_id']
    member = ColaboratorsFinder.get_from_external_id(member_external_id)
    member_name = member.name
    
    fileUp = TeamsHandler.get_image_member(member_name)
    
    if not fileUp:
        response = make_response(
        jsonify({
            'error': 'erro',
        })
        )
        return response
    
    response = make_response(
    jsonify({
        'error': '',
    })
    )
    return response
    
    
    


@bp.post("url")
@requires_client_auth
def create_team_member_test():
   
    file = request.files["fd"]
    name = request.form["name"]
    
    response = make_response(
    jsonify({
        'error': '',
    })
    )
    return response


@bp.post("/team/new-member")
@requires_client_auth
def create_team_member_vue():
    
    name = request.form["name"]
    external_id = request.form["external_id"]
    ist_id = request.form["ist_id"]
    email = request.form["email"]
    linkedin_url = request.form["linkedin_url"]    

    
    team = TeamsFinder.get_from_external_id(external_id)

    if team is None:
        if team is None:
            response = make_response(
            jsonify({
                'error': 'Couldnt find team',
            })
            )
            return response

    

    if len(ColaboratorsFinder.get_from_event_and_name(team.event_id, name)) > 0:
            response = make_response(
            jsonify({
                'error': 'Failed to create team member! Colaborator already exists',
            })
            )
            return response
        
    member = TeamsHandler.create_team_member(
        team=team, name=name, ist_id=ist_id, email=email, linkedin_url=linkedin_url
    )

    if member is None:
        response = make_response(
        jsonify({
            'error': 'Failed to create team member!',
        })
        )
        return response
    
    
    if "fd" in request.files:
        file = request.files["fd"]
        if file.filename:
            result, msg = TeamsHandler.upload_member_image(file, name)
            
            if result == False:
                TeamsHandler.delete_team_member(member)
                response = make_response(
                jsonify({
                    'error': msg,
                })
                )
                return response


    response = make_response(
    jsonify({
        'error': '',
    })
    )
    return response


@bp.post("/team/members/get_team_member")
@requires_client_auth
def get_team_member_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    external_id = response['external_id']
    member_external_id = response['member_external_id']
    team = TeamsFinder.get_from_external_id(external_id)

    if team is None:
        response = make_response(
        jsonify({
            'member': [],
            'image': '',
            'error': 'Couldnt find team',
        })
        )
        return response

    member = ColaboratorsFinder.get_from_external_id(member_external_id)

    if member is None:
        response = make_response(
        jsonify({
            'member': [],
            'image': '',
            'error': 'Couldnt find team member',
        })
        )
        return response

    image_path = TeamsHandler.find_member_image(member.name)
     
    member_vue = {
        "name": member.name,
        "ist_id": member.ist_id,
        "email": member.email,
        "linkedin_url": member.linkedin_url,
    }
    
    response = make_response(
    jsonify({
        'member': member_vue,
        'image': image_path,
        'error': '',
    })
    )
    return response

@bp.post("/team/update_team_member")
@requires_client_auth
def update_team_member_vue():
    
    name = request.form["name"]
    external_id = request.form["external_id"]
    ist_id = request.form["ist_id"]
    email = request.form["email"]
    linkedin_url = request.form["linkedin_url"]
    member_external_id = request.form["member_external_id"]
    
    team = TeamsFinder.get_from_external_id(external_id)

    if team is None:
        response = make_response(
        jsonify({
            'error': 'Couldnt find team',
        })
        )
        return response

    member = ColaboratorsFinder.get_from_external_id(member_external_id)

    if member is None:
        response = make_response(
        jsonify({
            'error': 'Couldnt find team member',
        })
        )
        return response


    old_member_name = member.name

    if len(ColaboratorsFinder.get_from_event_and_name(team.event_id, name)) > 1:
        response = make_response(
        jsonify({
            'error': 'Failed to create team member! Colaborator already exists',
        })
        )
        return response

    updated_member = TeamsHandler.update_team_member(
        member=member, name=name, ist_id=ist_id, email=email, linkedin_url=linkedin_url
    )

    image_path = TeamsHandler.find_member_image(name)

    if updated_member is None:
        response = make_response(
        jsonify({
            'error': 'Failed to update team member!',
        })
        )
        return response

    if old_member_name != name:
        RenameImageService("static/members", old_member_name, name).call()

    if "fd" in request.files:
        file = request.files["fd"]
        if file.filename:
            result, msg = TeamsHandler.upload_member_image(file, name)

            if result == False:
                response = make_response(
                jsonify({
                    'error': msg,
                })
                )
                return response
            
    response = make_response(
    jsonify({
        'error': '',
    })
    )
    return response


@bp.post("/team/delete_team_member")
@requires_client_auth
def delete_team_member_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    member_external_id = response['member_external_id']
    external_id = response['external_id']
    team = TeamsFinder.get_from_external_id(external_id)

    if team is None:
        response = make_response(
        jsonify({
            'error': 'Couldnt find team',
        })
        )
        return response

    member = ColaboratorsFinder.get_from_external_id(member_external_id)

    if member is None:
        response = make_response(
        jsonify({
            'error': 'Couldnt find team member',
        })
        )
        return response

    name = member.name

    if TeamsHandler.delete_team_member(member):
        response = make_response(
        jsonify({
            'error': '',
        })
        )
        return response

    else:
        image_path = TeamsHandler.find_member_image(name)
        response = make_response(
        jsonify({
            'error': 'Failed to delete team member!',
        })
        )
        return response
