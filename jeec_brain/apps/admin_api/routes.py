from flask import request, render_template, session, redirect, url_for, make_response, jsonify
from . import bp
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.activity_types_finder import ActivityTypesFinder
from jeec_brain.finders.students_finder import StudentsFinder

from flask_login import current_user
from jeec_brain.apps.auth.wrappers import allow_all_roles
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.handlers.events_handler import EventsHandler
from jeec_brain.finders.users_finder import UsersFinder

from jeec_brain.apps.auth.wrappers import requires_client_auth

import json

import logging

logger = logging.getLogger(__name__)

@bp.post("/_vue")
@requires_client_auth
def get_admin_login_form_vue():
    response = json.loads(request.data.decode('utf-8'))
    
    username = response['username']

    if username == "":
        error = ""
    else:
        user = UsersFinder.get_user_from_username(username)

        if user.is_authenticated and user.role in [
            "admin",
            "companies_admin",
            "speakers_admin",
            "teams_admin",
            "activities_admin",
            "viewer",
        ]:
            error = 'Error'
        else:
            error = ''

    response = make_response(jsonify(
            {'show': error}),
        )
    return response


@bp.post("/_vuee")
@requires_client_auth
def admin_login_vue():
    response = json.loads(request.data.decode('utf-8'))
    
    username = response['username']
    password = response['password']
    
    if AuthHandler.login_admin_dashboard(username, password) is False:
        return "Invalid credentials!"
    
    return ''

# content routes
@bp.get("/admin-logout_vue")
@requires_client_auth
def admin_logout_vue():
    error=''
    try:
        AuthHandler.logout_user()
        return error
    except:
        pass
        return 'Did not work'
    

# content routes
@bp.post("/dashboard_vue")
@requires_client_auth
def dashboard_vue():
    response = json.loads(request.data.decode('utf-8'))

    
    user = UsersFinder.get_user_from_username(response['username'])    
    
    event = EventsFinder.get_default_event()
    
    vue_activity_types = []
    for at in event.activity_types:
        vue_activity_types.append({'name': at.name})
    vue_event = {
        'name': event.name, 'external_id': event.external_id, 'activity_types': vue_activity_types,
    }
    
    logo = EventsHandler.find_image(image_name=str(event.external_id))
    
    if response['username'] == "":
        response = make_response(jsonify(
               {'error': 'Invalid','event': vue_event, 'logo': logo}),
            )
        return response
    if event == '':
        response = make_response(jsonify(
               {'error': 'Invalid','event': vue_event, 'logo': logo}),
            )
        return response
    
    response = make_response(jsonify(
               {'error': '', 'event': vue_event, 'logo': logo}),
            )
    return response
    

@bp.post("/login")
@requires_client_auth
def login_company_user():
    response = json.loads(request.data.decode('utf-8'))

    if response['username'] == "":
        return ""
    
    user = UsersFinder.get_user_from_username(response['username'])

    if user is None or user.role == 'company':
        return ""
    
    response = make_response(
        jsonify({
            "password":user.password,
            "role":user.role,
            "id":user.id
        })
    )
    return response



@bp.get("/")
@requires_client_auth
def get_admin_login_form():
    if current_user.is_authenticated and current_user.role in [
        "admin",
        "companies_admin",
        "speakers_admin",
        "teams_admin",
        "activities_admin",
        "viewer",
    ]:
        return redirect(url_for("admin_api.dashboard"))

    return render_template("admin/admin_login.html")


@bp.post("/")
@requires_client_auth
def admin_login():
    username = request.form.get("username")
    password = request.form.get("password")

    # if credentials are sent in json (for stress testing purposes)
    if not username and not password:
        username = request.json.get("username")
        password = request.json.get("password")

    if AuthHandler.login_admin_dashboard(username, password) is False:
        return render_template("admin/admin_login.html", error="Invalid credentials!")

    return redirect(url_for("admin_api.dashboard"))


# content routes
@bp.get("/admin-logout")
@requires_client_auth
def admin_logout():
    try:
        AuthHandler.logout_user()
    except:
        pass
    return redirect(url_for("admin_api.get_admin_login_form"))


# content routes
@bp.get("/dashboard")
@allow_all_roles
def dashboard():
    event = EventsFinder.get_default_event()
    if event is None:
        return render_template(
            "admin/dashboard.html", event=None, logo=None, user=current_user
        )

    logo = EventsHandler.find_image(image_name=str(event.external_id))
    return render_template(
        "admin/dashboard.html", event=event, logo=logo, user=current_user
    )

@bp.get("/getkings")
@requires_client_auth
def getkings():
    score_15 = [0]*600
    score_workshop = [0]*600
    score_job_fair = [0]*600
    score_palestras = [0]*600
    score_inside_talks = [0]*600
    all_students = StudentsFinder.get_all()
    activity_type_names = ['15/15','Inside Talks','Job Fair','Workshop','Main Speaker','Discussion Panel']
    for activity_type_name in activity_type_names:
        activity_type = ActivityTypesFinder.get_from_name(activity_type_name)
        activities = ActivitiesFinder.get_all_from_type(activity_type)
        for activity in activities:
            students = StudentsFinder.get_students_from_activity_id(activity.id)
            for student in students:
                if activity_type_name=='15/15':
             
                    score_15[student.id-190]+=1
                if activity_type_name=='Workshop':
           
                    score_workshop[student.id-190]+=1
                if activity_type_name=='Inside Talks':
               
                    score_inside_talks[student.id-190]+=1
                if activity_type_name=='Job Fair':
                
                    score_job_fair[student.id-190]+=1
                if activity_type_name=='Main Speaker':
                 
                    score_palestras[student.id-190]+=1
                if activity_type_name=='Discussion Panel':
                 
                    score_palestras[student.id-190]+=1
    max_15 = max(score_15)
    max_workshop = max(score_workshop)
    max_job_fair = max(score_job_fair)
    max_palestras = max(score_palestras)
    max_inside_talks = max(score_inside_talks)
    king_15 = ''
    king_workshop=''
    king_inside_talks=''
    king_palestras=''
    king_job_fair=''
    for index,score in enumerate(score_15):
        if(score==max_15):
            student = StudentsFinder.get_from_id(index+190)
            king_15+=student.user.name
            king_15+=' / '

    for index,score in enumerate(score_workshop):
        if(score==max_workshop):
            student = StudentsFinder.get_from_id(index+190)
            king_workshop+=student.user.name
            king_workshop+=' / '


    for index,score in enumerate(score_job_fair):
        if(score==max_job_fair):
            student = StudentsFinder.get_from_id(index+190)
            king_job_fair+=student.user.name
            king_job_fair+=' / '


    for index,score in enumerate(score_inside_talks):
        if(score==max_inside_talks):
            student = StudentsFinder.get_from_id(index+190)
            king_inside_talks+=student.user.name
            king_inside_talks+=' / '


    for index,score in enumerate(score_palestras):
        if(score==max_palestras):
            student = StudentsFinder.get_from_id(index+190)
            king_palestras+=student.user.name
            king_palestras+=' / '


    return make_response(
        jsonify({"king_15":king_15,
        "king_workshop":king_workshop,
        'king_inside_talks':king_inside_talks,
        'king_palestras':king_palestras,
        'king_job_fair':king_job_fair,
        })
        )