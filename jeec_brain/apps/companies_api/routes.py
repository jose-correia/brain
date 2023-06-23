from urllib import response
from flask import request, render_template, redirect, url_for, session,jsonify,make_response, send_file
from jeec_brain.apps.companies_api import bp
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.apps.auth.handlers.auth_handler import AuthHandler
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.auctions_finder import AuctionsFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.activity_types_finder import ActivityTypesFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.finders.users_finder import UsersFinder
from config import Config
from PIL import Image
from jeec_brain.apps.auth.wrappers import requires_client_auth

import json
import pickle
import os
import glob
import shutil
from dotenv import load_dotenv
import ast
from datetime import datetime

from jeec_brain.models.company_users import CompanyUsers


# @bp.get("/")
# def get_company_login_form():
#     if current_user.is_authenticated and current_user.role == "company":
#         return redirect(url_for("companies_api.dashboard"))

#     return render_template("companies/companies_login.html")


# @bp.post("/")
# def company_login():
#     username = request.form.get("username")
#     password = request.form.get("password")

#     # if credentials are sent in json (for stress testing purposes)
#     if not username and not password:
#         username = request.json.get("username")
#         password = request.json.get("password")

#     if AuthHandler.login_company(username, password) is False:
#         return render_template(
#             "companies/companies_login.html", error="Invalid credentials!"
#         )

#     return redirect(url_for("companies_api.dashboard"))


# @bp.get("/company-logout")
# def company_logout():
#     try:
#         AuthHandler.logout_user()
#     except:
#         pass
#     return redirect(url_for("companies_api.get_company_login_form"))


# @bp.get("/dashboard")
# @require_company_login
# def dashboard(company_user):
#     if not company_user.user.accepted_terms:
#         return render_template(
#             "companies/terms_conditions.html", user=company_user.user
#         )

#     now = datetime.now()
#     today = now.strftime("%d %b %Y, %a")

#     if company_user.company.cvs_access:
#         event = EventsFinder.get_default_event()
#         cvs_access_start = datetime.strptime(event.cvs_access_start, "%d %b %Y, %a")
#         cvs_access_end = datetime.strptime(event.cvs_access_end, "%d %b %Y, %a")
#         if now < cvs_access_start or now > cvs_access_end:
#             cvs_enabled = False
#         else:
#             cvs_enabled = True
#     else:
#         cvs_enabled = False

#     company_auctions = CompaniesFinder.get_company_auctions(company_user.company)
#     auctions = []
#     now = datetime.utcnow()
#     for company_auction in company_auctions:
#         end = datetime.strptime(
#             company_auction.closing_date + " " + company_auction.closing_time,
#             "%d %b %Y, %a %H:%M",
#         )
#         auction = company_auction._asdict()
#         auction["is_open"] = True if now < end else False
#         auctions.append(auction)

#     company_logo = CompaniesHandler.find_image(company_user.company.name)

#     activities = []
#     for activity in ActivitiesFinder.get_current_company_activities(
#         company_user.company
#     ):
#         if activity.day == today:
#             activities.append(activity)

#     return render_template(
#         "companies/dashboard.html",
#         auctions=auctions,
#         company_logo=company_logo,
#         activities=activities,
#         user=company_user,
#         cvs_enabled=cvs_enabled,
#     )

# @bp.post("/dashboard")
# @require_company_login
# def accept_terms(company_user):
#     print(39*"*")
#     UsersHandler.update_user(user=company_user.user, accepted_terms=True)

#     return redirect(url_for("companies_api.dashboard"))


# @bp.get("/chat")
# @require_company_login
# def chat(company_user):
#     chat_token = UsersHandler.get_chat_user_token(company_user.user)
#     chat_url = (
#         (Config.ROCKET_CHAT_APP_URL + "home?resumeToken=" + chat_token)
#         if chat_token
#         else None
#     )

#     return render_template("companies/chat/chat.html", user=company_user, chat_url=chat_url)

################################################################################
# login_company_user_vue() - checks if the username introduced is that of a    #
# company user, if it is, the backend sends the hashed password (stored in DB) #
# to be compared with what the user introduced as password. The comparison and # 
# dehashing is made by the frontend. The file name of the logo corresponding   #
# to the image of the company is also sent.                                    #
################################################################################


@bp.post("/login_vue")
@requires_client_auth
def login_company_user():
    response = json.loads(request.data.decode('utf-8'))
    if response['username'] == "":
        return ""
    
    user = UsersFinder.get_user_from_username(response['username'])
    company_user = CompanyUsers.query.filter_by(user_id=user.id).first()

    if user is []:
        print("No user found")
        return ""
    response = make_response(
        jsonify({
            "password":user.password,"company":company_user.company.name
        })
    )
    return response

################################################################################
# check_terms_vue() - Checks if the user has accepted the terms or not .        #
################################################################################
@bp.post("/terms_check_vue")
@requires_client_auth
def check_terms_vue():

    response = json.loads(request.data.decode('utf-8'))
    user = UsersFinder.get_user_from_username(response['user'])
    
    response = make_response(
        jsonify({
            "accepted_terms":user.accepted_terms
        })
    )
    return response

################################################################################
# accept_terms_vue() - If the user introduced the correct password to the      #
# respective username, the frontend will be redirected to a page displaying the#
# conditions and terms. The purpose of this endpoint is to update the status   #
# of the terms and conditions of a company user, since it is initialized as    #
# FALSE. This endpoint is reached when the user accepts the terms. This        #
# endpoint should only be reached once.                                        #
################################################################################
@bp.post("/terms")
@requires_client_auth
def accept_terms_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    user = UsersFinder.get_user_from_username(response['user'])
    company_user = CompanyUsers.query.filter_by(user_id=user.id).first()
    company = CompaniesFinder.get_from_company_id(company_user.company_id)
    UsersHandler.update_user(user=company_user.user, accepted_terms=True)

    return make_response(
        jsonify({
            "user_name": user.username,
            "company_name":company.name,
            "accepted_terms":user.accepted_terms
        }))

################################################################################
# dashboard_vue() - Sends the required information to the frontend to be       # 
# displayed. Receives as "argument" the user, which must be a company user.     #
################################################################################
@bp.post("/dashboard_vue")
@requires_client_auth
def dashboard_vue():
   
    response = json.loads(request.data.decode('utf-8'))
    if response['user'] is None:
        return make_response(
        jsonify({
            "error": "Not Allowed",
        }))
    user = UsersFinder.get_user_from_username(response['user'])
        
    company_user = CompanyUsers.query.filter_by(user_id=user.id).first()
    company = CompaniesFinder.get_from_company_id(company_user.company_id)
   
    now = datetime.now()
    today = now.strftime("%d %m %Y, %A")
    event = EventsFinder.get_default_event()
    if company_user.company.cvs_access:
        cvs_access_start = datetime.strptime(event.cvs_access_start, "%d %m %Y, %A")
        cvs_access_end = datetime.strptime(event.cvs_access_end, "%d %m %Y, %A")
        if now < cvs_access_start or now > cvs_access_end:
            cvs_enabled = False
        else:
            cvs_enabled = True
    else:
        cvs_enabled = False

    company_auctions = CompaniesFinder.get_company_auctions(company_user.company)
    auctions = []
    now = datetime.utcnow()
    for company_auction in company_auctions:
        end = datetime.strptime(
            company_auction.closing_date + " " + company_auction.closing_time,
            "%d %b %Y, %a %H:%M",
        )
        auction = company_auction._asdict()
        auction["is_open"] = True if now < end else False
        auctions.append(auction)
    
    activities = []
    for activity in ActivitiesFinder.get_current_company_activities(
        company_user.company
    ):
        if activity.day == today:
            activities.append(activity)

    activity_types = ActivityTypesFinder.get_all_from_event(event)

    activity_types_name = []
    for activity_type in activity_types:
        activity_types_name.append({"name": activity_type.name,"external_id":activity_type.external_id})
    
    response = make_response(
        jsonify({"user_name": user.username,
        "company_name":company.name,
        "food_manager":company_user.food_manager,
        "cvs_enabled":cvs_enabled,
        "activity_types_name":activity_types_name,
        "auctions":auctions
        })
    )

    return response

@bp.post("/company/image")
@requires_client_auth
def getimagecompany_vue():
    
    response = json.loads(request.data.decode('utf-8'))
    company_name = response['company']
    
    fileUp = CompaniesHandler.get_image(company_name)
    

    if not fileUp:
        return '',404
    
    filedown = Image.open(fileUp)
    print(filedown)
 
    return send_file(
        fileUp
    )


@bp.post("/changepassword")
@requires_client_auth
def change_password():
    response = json.loads(request.data.decode('utf-8'))
    username = response['username']
    new_password = response['new_password']

    user = UsersFinder.get_user_from_username(username)

    if user is None:
        return "Invalid credentials!", 200

    company_user = UsersFinder.get_company_user_from_user(user)
    if company_user is None:
        return "Invalid credentials!", 200

    if user.role != "company" or company_user.company is None:
        return "Invalid credentials!", 200

    if(UsersHandler.change_password(user,new_password)):
        return '',204
    return 'Password change unsuccesfull', 200

@bp.post("/getpassword")
@requires_client_auth
def get_password():
    response = json.loads(request.data.decode('utf-8'))
    username = response['username']
    user = UsersFinder.get_user_from_username(username)
    if user is None:
        return "User not found", 404
    return user.password, 200
    
         
         
         
         
         
         
         
         
         

    
        

