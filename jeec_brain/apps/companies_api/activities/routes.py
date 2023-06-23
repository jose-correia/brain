from jeec_brain.apps.companies_api import bp
from flask import render_template, session, request, redirect, url_for, jsonify,jsonify,make_response
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.finders.quests_finder import QuestsFinder
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.handlers.activities_handler import ActivitiesHandler
from jeec_brain.finders.activity_types_finder import ActivityTypesFinder
from jeec_brain.finders.activity_codes_finder import ActivityCodesFinder
from jeec_brain.handlers.activity_codes_handler import ActivityCodesHandler
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.handlers.students_handler import StudentsHandler
from jeec_brain.models.company_users import CompanyUsers
from jeec_brain.models.enums.code_flow_enum import CodeFlowEnum
from jeec_brain.handlers.reward_student_handler import StudentRewardsHandler
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.companies_api.activities.schemas import *
from datetime import datetime
from config import Config
import json
from jeec_brain.apps.auth.wrappers import requires_client_auth

def check_quest(quests, student,activity, today):
    for quest in quests:
        if quest.day == today:
    #activity type id == -1 
            if quest.activity_type_id == -1:
                list_of_activities_id = quest.activities_id
                student_list_of_activities = StudentsFinder.get_student_activities_from_student_id(student.id)
                activities_id = []
                for activity in student_list_of_activities:
                    activities_id.append(activity.id)
                if(set(list_of_activities_id).issubset(set(activities_id))) and activity.id in list_of_activities_id:
                    StudentRewardsHandler.add_reward_student(reward=quest.reward_id,student=student.id)
            else:
                activity_type = ActivityTypesFinder.get_from_activity_type_id(quest.activity_type_id)
                activities_of_activity_type = ActivitiesFinder.get_all_from_type(activity_type=activity_type)
                student_list_of_activities = StudentsFinder.get_student_activities_from_student_id(student.id)
                count = 0
                for elem1 in student_list_of_activities:
                    for elem2 in activities_of_activity_type:
                        if elem1.activity_id == elem2.id:
                            count += 1
                if count == quest.number_of_activities:
                    StudentRewardsHandler.add_reward_student(reward=quest.reward_id,student_id=student.id)
    return


@bp.get("/activity/<string:activity_external_id>")
@require_company_login
def get_activity_type(company_user, path: ActivityPath):
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    if activity is None:
        return APIErrorValue("No activity found").json(404)

    return render_template(
        "companies/activities/activity.html",
        activity=activity,
        error=None,
        user=company_user,
    )


@bp.post("/activity/<string:activity_external_id>/code")
@require_company_login
def generate_code(company_user, path: ActivityPath):
    now = datetime.utcnow()
    today = now.strftime("%d %m %Y, %A")

    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    if (
        activity.code_work_flow
        in [CodeFlowEnum.CompanyMultiUseCode, CodeFlowEnum.CompanyOneUseCode]
        and activity.day == today
    ):
        activity_code = ActivityCodesHandler.create_activity_code(
            activity_id=activity.id
        )

        return jsonify(activity_code.code)

    return APIErrorValue("Not allowed").json(401)


@bp.post("/activity/<string:activity_external_id>/istid")
@require_company_login
def use_istid(company_user, path: ActivityPath):
    now = datetime.utcnow()
    today = now.strftime("%d %m %Y, %A")

    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    if activity.code_work_flow in [CodeFlowEnum.CompanyISTID] and activity.day == today:
        ist_id = request.form.get("istid")
        student = StudentsFinder.get_from_ist_id(ist_id)
        if not student:
            return APIErrorValue("Student not found").json(401)

        student_activity = ActivitiesHandler.add_student_activity(
            student, activity, ist_id, company_user.company
        )
        if student_activity:
            StudentsHandler.add_points(student, activity.points)

            return jsonify(f"Code scanned successfully, for {student.user.name}")

        return APIErrorValue("Failed to redeem code").json(500)

    return APIErrorValue("Not allowed").json(401)


################################################################################
# activitiesdashboard_vue() - Receives as argument the user and retrieves the  #
# company from it. From the company, it gets for the activities that the       #
# company is enrolled in and are happening today. Sends to the frontend        #
# information relative to the activities found.
################################################################################

@bp.post("/dashboard_vue/activitiesdashboard_vue")
@requires_client_auth
def activitiesdashboard_vue():
   
    response = json.loads(request.data.decode('utf-8'))
    user = UsersFinder.get_user_from_username(response['user'])
    company_user = CompanyUsers.query.filter_by(user_id=user.id).first()
    company = CompaniesFinder.get_from_company_id(company_user.company_id)
    now = datetime.now()
    today = now.strftime("%d %m %Y, %A")  # 17 02 2023, Friday

    activities = []
   
    for activity in ActivitiesFinder.get_current_company_activities(company_user.company):
        
        if activity.day == today:
            activities.append({"name":activity.name,
            "activity_type":ActivityTypesFinder.get_from_activity_type_id(activity.activity_type_id).name,
            "description":activity.description,
            "day":activity.day,
            "time":activity.time,
            "location":activity.location,
            "activity_ex_id":activity.external_id})
            
    error = ""
    if activities == []:
        error = "No activities were found!"
    
    
 
    response = make_response(
        jsonify({"user_name": user.username,
        "company_name":company.name,
        "activities":activities,
        "error": error
        
        })
    )

    return response


################################################################################
# activitydetail_vue() - Receives as argument the user and the activity's      #
# external id. Loads the activity in question from this last parameter. The    #
# purpose of this endpoint is to feed the frontend with more details of the    #
# activity such as the registration link etc.                                  #
################################################################################

@bp.post("/activitiesdashboard_vue/activity")
@requires_client_auth
def activitydetail_vue():

    response = json.loads(request.data.decode('utf-8'))
    user = UsersFinder.get_user_from_username(response['user'])
    company_user = CompanyUsers.query.filter_by(user_id=user.id).first()
    company = CompaniesFinder.get_from_company_id(company_user.company_id)
    activity_external_id = response['activity_external_id']
    activity = ActivitiesFinder.get_from_external_id(activity_external_id)

    if activity == None:
        return make_response(
        jsonify({"user_name": user.username,
        "company_name":company.name,
        "error": "This activity does not exist"
        })
    )

    response = make_response(
        jsonify({"user_name": user.username,
        "company_name":company.name,
        "activity":{
            "location":activity.location,
            "name":activity.name,
            "day":activity.day,
            "time":activity.time,
            "registration_link":activity.registration_link,
            "registration_open":activity.registration_open,
            "description":activity.description,
        }
        })
    )
    
    return response





################################################################################
# use_istid_vue() - Receives as argument the user, the activity's external id  #
# and the id of the student. Both the student id and the activity's external id#
# come in the same string from the frontend a preprocessing is needed.         #
# The activity external id is 36 characters long, so the rest of the string    #
# will be the ist id. We check if the student exists and also if he hasn't been#
# added to the activity already. This is only valid for activities happening at#
# "today".
################################################################################

@bp.post("/activitiesdashboard_vue/activity/activity_external_idistid")
@requires_client_auth
def use_istid_vue():
    now = datetime.utcnow()
    today = now.strftime("%d %m %Y, %A")
    
    response = json.loads(request.data.decode('utf-8'))
    activity_ex_id = response['activity_external_idistid']
    if(len(activity_ex_id)!=72):
        return make_response(
            jsonify({"student_username":"",
            "errorQR":"The scanned student does not exist"
            }))
    activity_external_id = activity_ex_id[0:36]
    external_id = activity_ex_id[36:len(activity_ex_id)]
    activity = ActivitiesFinder.get_from_external_id(activity_external_id)

    
    if activity.day == today:
        student = StudentsFinder.get_from_external_id(external_id)
        if not student:
            return make_response(
            jsonify({"student_username":"",
            "errorQR":"The scanned student does not exist"
            })
        )

        student_activity = ActivitiesHandler.add_student_activity(
            student, activity, student.user.username
        )
        if student_activity is not None:
            StudentsHandler.add_points(student, activity.points)
            quest = QuestsFinder.get_all()
            check_quest(quests=quest, student=student,activity=activity,today=today)
            
          
            return make_response(
            jsonify({"student_username":student.user.name,
            "errorQR":""
            })
            )
        else:
            print("activity had already been added ")
            return make_response(
                jsonify({"student_username":"",
                "errorQR":"Failed to redeem code"
                })
                )

    return make_response(
        jsonify({"student_username":"",
        "errorQR":"Not Allowed"
        })
        )


################################################################################
# activitytype_vue() - Receives as argument the user and the activity's type   #
# external id. The purpose of this endpoint is to send the frontend all the    #
# activities of a certain type. The length verifier is to prevent meddling with#
# the URL.  
################################################################################
@bp.post("/activitiesdashboard_vue/activity_type")
@requires_client_auth
def activitytype_vue():
    
    event = EventsFinder.get_default_event()
    response = json.loads(request.data.decode('utf-8'))
    user = UsersFinder.get_user_from_username(response['user'])
    company_user = CompanyUsers.query.filter_by(user_id=user.id).first()
    company = CompaniesFinder.get_from_company_id(company_user.company_id)
    activity_type_external_id = response['activity_type_external_id']

    if len(activity_type_external_id) != 36:
     
        return make_response(
            jsonify({"user_name": user.username,
            "company_name":company.name,
            "error": "Couldn't find activity type, this might be due to an URL being manually changed",
            "valid": False
            })
        )

    activities = ActivitiesFinder.get_all_from_type(ActivityTypesFinder.get_from_external_id(activity_type_external_id))
    if len(activities) == 0 :
        return make_response(
            jsonify({"user_name": user.username,
            "company_name":company.name,
            "error": "Couldn't find any activity of this type",
            "valid": False
            })
        )

    activities_json = []
    for activity in activities:
        activities_json.append({
            "name":activity.name,
            "description":activity.description,
            "day":activity.day,
            "time":activity.time,
            "end_time":activity.end_time,
            "registration_link":activity.registration_link,
            "registration_open":activity.registration_open
        })

    response = make_response(
        jsonify({
        "user_name": user.username,
        "company_name":company.name,
        "activities": activities_json,
        "event_name":event.name,
        "error": "",
        "valid": True
        })
    )
    
    return response
    