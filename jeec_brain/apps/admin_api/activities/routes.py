import random
from jeec_brain.handlers.students_handler import StudentsHandler
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.schemas.admin_api.activities.schemas import (
    ActivityPath,
    ActivityTypePath,
    CodePath,
)
from .. import bp
import uuid
from flask import render_template, current_app, request, redirect, url_for, jsonify, make_response
from flask_login import current_user
from datetime import datetime
import json

from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.activity_types_finder import ActivityTypesFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.speakers_finder import SpeakersFinder
from jeec_brain.finders.tags_finder import TagsFinder
from jeec_brain.finders.rewards_finder import RewardsFinder
from jeec_brain.handlers.tags_handler import TagsHandler
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.finders.activity_codes_finder import ActivityCodesFinder
from jeec_brain.finders.quests_finder import QuestsFinder
from jeec_brain.handlers.activities_handler import ActivitiesHandler
from jeec_brain.handlers.activity_types_handler import ActivityTypesHandler
from jeec_brain.handlers.activity_codes_handler import ActivityCodesHandler
from jeec_brain.handlers.quests_handler import QuestsHandler
from jeec_brain.handlers.reward_student_handler import StudentRewardsHandler
from jeec_brain.models.enums.activity_chat_enum import ActivityChatEnum
from jeec_brain.models.enums.code_flow_enum import CodeFlowEnum
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.finders.rewards_finder import RewardsFinder
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
from jeec_brain.schemas.admin_api.activities import *
from config import Config
from jeec_brain.apps.auth.wrappers import requires_client_auth

def check_quest(quests, student,activity, today):
    for quest in quests:
        if quest.day == today:
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


# Activities routes
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
            quests = QuestsFinder.get_all()
            check_quest(quests, student, activity, today)
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

@bp.post("/activity/qrcode")
@requires_client_auth
def activitydetail_vue():
    response = json.loads(request.data.decode('utf-8'))
    user = UsersFinder.get_user_from_username(response['user'])
    activity_external_id = response['activity_external_id']
    activity = ActivitiesFinder.get_from_external_id(activity_external_id)
 
    if activity == None:
        return make_response(
        jsonify({"user_name": user.username,
        "error": "This activity does not exist"
        })
    )
    

    response = make_response(
        jsonify({
            "user_name": user.username,
        "activity":{
            "location":activity.location,
            "name":activity.name,
            "day":activity.day,
            "time":activity.time,
            "registration_link":activity.registration_link,
            "registration_open":activity.registration_open,
            "description":activity.description,
        },
        'error': ''
        })
    )
    return response
    
# Activities routes
# @allow_all_roles
@bp.post("/activities_vue")
@requires_client_auth
def activities_dashboard_vue():
    response = json.loads(request.data.decode('utf-8'))
    
    now = datetime.utcnow()
    today = now.strftime("%d %m %Y, %A")
    # get event
    event_id = response['event_id']

    if event_id == '':
        event_getted = EventsFinder.get_default_event()
    else:
        event_getted = EventsFinder.get_from_external_id(event_id)
    
    activity_types_event = []
    for activity_type in event_getted.activity_types:
        vue_activity_type_event = {
            "name": activity_type.name,
            "description": activity_type.description,
            'external_id': activity_type.external_id,
            'price': activity_type.price, 
            'show_in_home': activity_type.show_in_home, 
            'show_in_schedule': activity_type.show_in_schedule, 
            'show_in_app': activity_type.show_in_app,
        }
        activity_types_event.append(vue_activity_type_event)
        
    event_new = {
    "name": event_getted.name,
    "activity_types": activity_types_event, "external_id": event_getted.external_id,
    }

    events_list = EventsFinder.get_all()

    events = []
    for event in events_list:
        activity_types = []
        for activity_type in event.activity_types:
            vue_activity_type = {"name": activity_type.name, "external_id": activity_type.external_id}
            activity_types.append(vue_activity_type)
        vue_event = {
        "name": event.name,
        "activity_types": activity_types, "external_id": event.external_id,
        }
        events.append(vue_event)
    
    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'event': '', 'events': events,
            'activities': '', 'error': error,
            'role': '', 'today': today,
            }),
        )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])

    if event_new == '':
        error = 'No default event found! Please set a default event in the menu "Events"'
        response = make_response(jsonify(
            {'event': '', 'events': events,
            'activities': '', 'error': error,
            'role': user.role,'today': today,
            }),
        )
        return response
    

    activities_list = event.activities

    if not activities_list:
        error = "No results found"
        
        response = make_response(jsonify(
            {'event': event_new,
            'events': events,
            'activities': '',
            'error': error,
            'role': user.role, 'today': today,
            }),
        )
        return response
    
    activities = []
    for activity in activities_list:
        activity_type_vue = {
            "name": activity.activity_type.name,
            "description": activity.activity_type.description,
            'external_id': activity.activity_type.external_id,
            'price': activity.activity_type.price, 
            'show_in_home': activity.activity_type.show_in_home, 
            'show_in_schedule': activity.activity_type.show_in_schedule, 
            'show_in_app': activity.activity_type.show_in_app,
        }
        # code_work_flow_vue = {
        #    "value": activity.code_work_flow.value,
        # }
        reward_id = activity.reward_id
        reward = RewardsFinder.get_reward_from_id(reward_id)
        
        moderator_id = activity.moderator_id
        
        if activity.chat_type != None:
            chat_type = activity.chat_type.name
        else:
            chat_type = 'No'
        
        vue_activity = {
        'name': activity.name,
        "id": activity.id,
        "description": activity.description,
        "day": activity.day,
        "time": activity.time,
        "end_time": activity.end_time,
        "location": activity.location,
        "points": activity.points,
        "quest": activity.quest,
        "activity_type": activity_type_vue,
        # "code_work_flow": code_work_flow_vue,
        'registration_link': activity.registration_link,
        'registration_open': activity.registration_open, 
        'chat_type': {'name': chat_type},
        'chat': activity.chat_id, 
        'zoom_link': activity.zoom_link, 
        'reward_id': reward_id,
        'moderator_id': moderator_id,
        'external_id': activity.external_id,
        'volunteers': activity.volunteers_id
        # 'code_per_company': activity.code_per_company,
        }
              
        activities.append(vue_activity)
    
    response = make_response(jsonify(
        {'event': event_new,
        'events': events,
        'activities': activities,
        'error': '',
        'role': user.role, 'today': today,
        }),
    )
    return response


# Activities Types routes
# @allow_all_roles
@bp.post("/activities/types-get_vue")
@requires_client_auth
def activity_types_dashboard_vue():
    response = json.loads(request.data.decode('utf-8'))
        
    events_list = EventsFinder.get_all()

    event_id = response['event_id']
    if event_id == '':
        event_getted = EventsFinder.get_default_event()
    else:
        event_getted = EventsFinder.get_from_external_id(event_id)

    activity_types_event = []
    for activity_type in event_getted.activity_types:
        vue_activity_type_event = {
            "name": activity_type.name,
            "description": activity_type.description,
            'external_id': activity_type.external_id,
            'price': activity_type.price, 
            'show_in_home': activity_type.show_in_home, 
            'show_in_schedule': activity_type.show_in_schedule, 
            'show_in_app': activity_type.show_in_app,
        }
        activity_types_event.append(vue_activity_type_event)
        
    event_new = {
    "name": event_getted.name,
    "activity_types": activity_types_event, "external_id": event_getted.external_id,
    }
    
    events = []
    for event in events_list:
        activity_types = []
        for activity in event.activity_types:
            vue_activity = {"name": activity.name, "external_id": activity.external_id}
            activity_types.append(vue_activity)
        vue_event = {
        "name": event.name,
        "activity_types": activity_types, "external_id": event.external_id,
        }
        events.append(vue_event)

    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'event': '',
            'events': events,
            'error': error,
            'role': '',
            }),
        )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    if event_new == '':
        error = 'No default event found! Please set a default event in the menu "Events"'
        
        response = make_response(jsonify(
            {'event': '',
            'events': events,
            'error': error,
            'role': user.role,
            }),
        )
        return response
            
    response = make_response(jsonify(
        {'event': event_new,
        'events': events,
        'error': '',
        'role': user.role,
        }),
    )
    return response

# @allow_all_roles
@bp.post("/activities/types_vue")
@requires_client_auth
def search_activity_types_vue():
    response = json.loads(request.data.decode('utf-8'))
        
    events_list = EventsFinder.get_all()

    event = response['event'] 
    if event == '':
        event_getted = EventsFinder.get_default_event()
    else:
        event_getted = EventsFinder.get_from_external_id(event)

    activity_types_event = []
    for activity_type in event_getted.activity_types:
        vue_activity_type_event = {
            "name": activity_type.name,
            "description": activity_type.description,
            'external_id': activity_type.external_id,
            'price': activity_type.price, 
            'show_in_home': activity_type.show_in_home, 
            'show_in_schedule': activity_type.show_in_schedule, 
            'show_in_app': activity_type.show_in_app,
        }
        activity_types_event.append(vue_activity_type_event)
        
    event_new = {
    "name": event_getted.name,
    "activity_types": activity_types_event, "external_id": event_getted.external_id,
    }
    
    events = []
    for event in events_list:
        activity_types = []
        for activity in event.activity_types:
            vue_activity = {"name": activity.name, "external_id": activity.external_id}
            activity_types.append(vue_activity)
        vue_event = {
        "name": event.name,
        "activity_types": activity_types, "external_id": event.external_id,
        }
        events.append(vue_event)
    
    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'events': events,
            'event': '',
            'error': error,
            'role': '',
            }),
        )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    if event_new == '':
        error = 'No event found! Please set an event in the menu "Events"'
        response = make_response(jsonify(
            {'events': events,
            'event': '',
            'error': error,
            'role': user.role,
            }),
        )
        return response

    response = make_response(jsonify(
        {'events': events,
        'event': event_new,
        'error': '',
        'role': user.role,
        }),
    )
    return response

# @allowed_roles(["admin", "activities_admin"])
@bp.post("/new-activity-type-dashboard_vue")
@requires_client_auth
def add_activity_type_dashboard_vue():
    response = json.loads(request.data.decode('utf-8'))
    
    event_id = response['event_id']
    if event_id == '':
        event_getted = EventsFinder.get_default_event()
    else:
        event_getted = EventsFinder.get_from_external_id(event_id)
        
    activity_types_event = []
    for activity_type in event_getted.activity_types:
        vue_activity_type_event = {
            "name": activity_type.name,
            "description": activity_type.description,
            'external_id': activity_type.external_id,
            'price': activity_type.price, 
            'show_in_home': activity_type.show_in_home, 
            'show_in_schedule': activity_type.show_in_schedule, 
            'show_in_app': activity_type.show_in_app,
        }
        activity_types_event.append(vue_activity_type_event)
        
    event_new = {
    "name": event_getted.name,
    "activity_types": activity_types_event, "external_id": event_getted.external_id,
    }
    
    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'event': event_new, 
            'error': error}),
        )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    #if user.role != 'admin' and user.role != 'activities_admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #        {'event': event_new, 
    #        'error': error}),
    #    )
    #    return response
    
    if event_new == '':
        error = 'No event found! Please set an event in the menu "Events"'
        response = make_response(jsonify(
            {'event': '', 
            'error': error}),
        )
        return response

    response = make_response(jsonify(
        {'event': event_new, 
         'error': ''}),
    )
    return response


# @allowed_roles(["admin", "activities_admin"])
@bp.post("/new-activity-type_vue")
@requires_client_auth
def create_activity_type_vue():
    response = json.loads(request.data.decode('utf-8'))
    
    name = response['name']
    description = response['description']
    price = response['price']
    show_in_home = response['show_in_home']
    show_in_schedule = response['show_in_schedule']
    show_in_app = response['show_in_app']
    

    if show_in_home == "true":
        show_in_home = True
    else:
        show_in_home = False

    if show_in_schedule == "true":
        show_in_schedule = True
    else:
        show_in_schedule = False

    if show_in_app == "true":
        show_in_app = True
    else:
        show_in_app = False

    event_id = response['event_id']
    if event_id == '':
        event_getted = EventsFinder.get_default_event()
    else:
        event_getted = EventsFinder.get_from_external_id(event_id)
    
    activity_types_event = []
    for activity_type in event_getted.activity_types:
        vue_activity_type_event = {
            "name": activity_type.name,
            "description": activity_type.description,
            'external_id': activity_type.external_id,
            'price': activity_type.price, 
            'show_in_home': activity_type.show_in_home, 
            'show_in_schedule': activity_type.show_in_schedule, 
            'show_in_app': activity_type.show_in_app,
        }
        activity_types_event.append(vue_activity_type_event)
        
    event_new = {
    "name": event_getted.name,
    "activity_types": activity_types_event, "external_id": event_getted.external_id,
    }
    
    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'event': event_new,
            'error': error}),
        )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    #if user.role != 'admin' and user.role != 'activities_admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #        {'event': event_new,
    #        'error': error}),
    #    )
    #    return response
    
    if event_new == '':
        response = make_response(jsonify(
            {'event': event_new,
            'error': 'No event found! Please set an event in the menu "Events"'}),
        )
        return response

    activity_type = ActivityTypesHandler.create_activity_type(
        event=event_getted,
        name=name,
        description=description,
        price=price,
        show_in_home=show_in_home,
        show_in_schedule=show_in_schedule,
        show_in_app=show_in_app,
    )

    if activity_type == '':
        response = make_response(jsonify(
            {'event': event_new,
            'error': "Failed to create activity type! Maybe it already exists :)"}),
        )
        return response

    response = make_response(jsonify(
        {'event': event_new,
        'error': ""}),
    )
    return response

# @allowed_roles(["admin", "activities_admin"])
@bp.post("/activities/types/get_activity_type_vue")
@requires_client_auth
def get_activity_type_vue():
    response = json.loads(request.data.decode('utf-8'))
    activity_type_external_id = response['activity_type_external_id']
    activity_type = ActivityTypesFinder.get_from_external_id(
        activity_type_external_id
    )
    
    activity_type_vue = {
        "name": activity_type.name,
        "description": activity_type.description,
        'external_id': activity_type.external_id,
        'price': activity_type.price, 
        'show_in_home': activity_type.show_in_home, 
        'show_in_schedule': activity_type.show_in_schedule, 
        'show_in_app': activity_type.show_in_app,
    }

    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
        {'activity_type': activity_type_vue,
            'error': error}),
        )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    #if user.role != 'admin' and user.role != 'activities_admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #    {'activity_type': activity_type_vue,
    #        'error': error}),
    #    )
    #    return response

    response = make_response(jsonify(
        {'activity_type': activity_type_vue,
        'error': ''}),
    )
    return response

# @allowed_roles(["admin", "activities_admin"])
@bp.post("/activities/types/update_vue")
@requires_client_auth
def update_activity_type_vue():
    response = json.loads(request.data.decode('utf-8'))
    activity_type_external_id = response['activity_type_external_id']
    name = response['name']
    description = response['description']
    price = response['price']
    show_in_home = response['show_in_home']
    show_in_schedule = response['show_in_schedule']
    show_in_app = response['show_in_app']

    if show_in_home == "true":
        show_in_home = True
    else:
        show_in_home = False

    if show_in_schedule == "true":
        show_in_schedule = True
    else:
        show_in_schedule = False

    if show_in_app == "true":
        show_in_app = True
    else:
        show_in_app = False

    activity_type = ActivityTypesFinder.get_from_external_id(
        activity_type_external_id
    )

    updated_activity_type = ActivityTypesHandler.update_activity_type(
        activity_type=activity_type,
        name=name,
        description=description,
        price=price,
        show_in_home=show_in_home,
        show_in_schedule=show_in_schedule,
        show_in_app=show_in_app,
    )
    
    activity_type_vue = {
        "name": activity_type.name,
        "description": activity_type.description,
        'external_id': activity_type.external_id,
        'price': activity_type.price, 
        'show_in_home': activity_type.show_in_home, 
        'show_in_schedule': activity_type.show_in_schedule, 
        'show_in_app': activity_type.show_in_app,
    }

    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'activity_type': activity_type_vue,
            'error': error}),
        )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    #if user.role != 'admin' and user.role != 'activities_admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #        {'activity_type': activity_type_vue,
    #        'error': error}),
    #    )
    #    return response
    
    if updated_activity_type == '':
        response = make_response(jsonify(
            {'activity_type': activity_type_vue,
            'error': "Failed to update activity type!"}),
        )
        return response

    response = make_response(jsonify(
        {'activity_type': activity_type_vue,
        'error': ""}),
    )
    return response

# @allowed_roles(["admin", "activities_admin"])
@bp.post("/activities/types/delete_vue")
@requires_client_auth
def delete_activity_type_vue():
    response = json.loads(request.data.decode('utf-8'))
    
    activity_type_external_id = response['activity_type_external_id']
    activity_type = ActivityTypesFinder.get_from_external_id(
        activity_type_external_id
    )
    
    activity_type_vue = {
        "name": activity_type.name,
        "description": activity_type.description,
        'external_id': activity_type.external_id,
        'price': activity_type.price, 
        'show_in_home': activity_type.show_in_home, 
        'show_in_schedule': activity_type.show_in_schedule, 
        'show_in_app': activity_type.show_in_app,
    }
    
    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'activity_type': activity_type_vue,
            'error': error}),
        )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    #if user.role != 'admin' and user.role != 'activities_admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #        {'activity_type': activity_type_vue,
    #        'error': error}),
    #    )
    #    return response

    if activity_type.activities:
        for activity in activity_type.activities:
            if activity == '':
                error = "Couldnt find activity"
                response = make_response(jsonify(
                    {'activity_type': activity_type_vue,
                    'error': error}),
                )
                return response
                

            company_activities = (
                ActivitiesFinder.get_company_activities_from_activity_id(
                    activity.external_id
                )
            )
            speaker_activities = (
                ActivitiesFinder.get_speaker_activities_from_activity_id(
                    activity.external_id
                )
            )

            if company_activities:
                for company_activity in company_activities:
                    ActivitiesHandler.delete_company_activities(company_activity)

            if speaker_activities:
                for speaker_activity in speaker_activities:
                    ActivitiesHandler.delete_speaker_activities(speaker_activity)

            if not ActivitiesHandler.delete_activity(
                Config.ROCKET_CHAT_ENABLE, activity
            ):
                error = "Couldnt delete activity"
                response = make_response(jsonify(
                    {'activity_type': activity_type_vue,
                    'error': error}),
                )
                return response

    if ActivityTypesHandler.delete_activity_type(activity_type):
        response = make_response(jsonify(
            {'activity_type': activity_type_vue,
            'error': ""}),
        )
        return response

    response = make_response(jsonify(
        {'activity_type': activity_type_vue,
        'error': "Failed to update activity type!"}),
    )
    return response

# @allowed_roles(["admin", "activities_admin"])
@bp.post("/new-activity-get_vue")
@requires_client_auth
def add_activity_dashboard_vue():
    response = json.loads(request.data.decode('utf-8'))

    companies = CompaniesFinder.get_all()
    speakers = SpeakersFinder.get_all()
    tags = TagsFinder.get_all()
    rewards = RewardsFinder.get_all_rewards()
    volunteers = UsersFinder.get_all_users_by_role("team")

    vue_volunteers=[]

    for volunteer in volunteers:
        vue_volunteer = {
            'name':volunteer.name,
            'id':volunteer.id
        }
        vue_volunteers.append(vue_volunteer)

    event_id = response['event_id']
    if event_id == '':
        event_getted = EventsFinder.get_default_event()
    else:
        event_getted = EventsFinder.get_from_external_id(event_id)

    activity_types_event = []
    for activity_type in event_getted.activity_types:
        vue_activity_type_event = {
            "name": activity_type.name,
            "description": activity_type.description,
            'external_id': activity_type.external_id,
            'price': activity_type.price, 
            'show_in_home': activity_type.show_in_home, 
            'show_in_schedule': activity_type.show_in_schedule, 
            'show_in_app': activity_type.show_in_app,
        }
        activity_types_event.append(vue_activity_type_event)
        
    event_new = {
    "name": event_getted.name,
    "activity_types": activity_types_event, "external_id": event_getted.external_id,
    }
    
    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'event': '',
            'error': error,
            'role': '',
            }),
        )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    #if user.role != 'admin' and user.role != 'activities_admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #        {'event': '',
    #        'error': error,
    #        'role': '',
    #        }),
    #    )
    #    return response

    if event_new == '':
        error = 'No default event found! Please set a default event in the menu "Events"'
        
        response = make_response(jsonify(
            {'event': '',
            'error': error,
            'role': user.role,
            }),
        )
        return response

    try:
        minDate = datetime.strptime(event_new.start_date, "%d %b %Y, %a").strftime("%Y,%m,%d")
        maxDate = datetime.strptime(event_new.end_date, "%d %b %Y, %a").strftime("%Y,%m,%d")
    except:
        minDate = ''
        maxDate = ''

    vue_companies = []
    for comp in companies:
        vue_companies.append({"name": comp.name, "external_id": comp.external_id})
    
    vue_speakers = []
    for sp in speakers:
        vue_speakers.append({"name": sp.name, "external_id": sp.external_id})
    
    vue_tags = []
    for tg in tags:
        vue_tags.append({"name": tg.name, "external_id": tg.external_id})
    
    vue_rewards = []
    for rw in rewards:
        vue_rewards.append({"name": rw.name, "external_id": rw.external_id})
    
    # vue_codeworkflows = []
    # for cf in CodeFlowEnum:
    #     vue_codeworkflows.append({"value": cf.value})
            
    response = make_response(jsonify(
        {'companies': vue_companies,
        'speakers': vue_speakers,
        'tags': vue_tags,
        'minDate': minDate,
        'maxDate': maxDate,
        'event': event_new,
        'rewards': vue_rewards,
        'volunteers': vue_volunteers,
        # 'code_workflows': vue_codeworkflows,
        'error': ''}),
    )
    return response

# @allowed_roles(["admin", "activities_admin"])
@bp.post("/new-activity_vue")
@requires_client_auth
def create_activity_vue():
    response = json.loads(request.data.decode('utf-8'))
    name = response['name']
    description = response['description']
    location = response['location']
    day = response['day']
    time = response['time']
    end_time = response['end_time']
    points = response['points'] 
    registration_link = response['registration_link']
    registration_open = response['registration_open']
    try:
        volunteers = response['volunteers']
    except:
        volunteers = []
    volunteers_to_send = []
    for volunteer in volunteers:
        volunteers_to_send.append(volunteer['id'])

    print(response['reward_external_id'] )
    try:
        reward_external_id = response['reward_external_id'] 
    except:
        reward_external_id = ''
    if reward_external_id != '':
        reward = RewardsFinder.get_reward_from_external_id(reward_external_id)
        reward_id = reward.id
    else: 
        reward = ''
        reward_id = None
    moderator_external_id = response['moderator_external_id'] 
    if moderator_external_id != '':
        moderator = SpeakersFinder.get_from_external_id(moderator_external_id)
    else: 
        moderator = ''

    activity_type_external_id = response['activity_type_external_id']
    print(activity_type_external_id)
    
    if activity_type_external_id == '':
        error = 'Not valid activity_type'
        response = make_response(jsonify(
            {'event': '',
            'error': error,
            'role': '',
            }),
        )
        return response
    
    activity_type = ActivityTypesFinder.get_from_external_id(activity_type_external_id)
    if registration_open == "true":
        registration_open = True
    else:
        registration_open = False



  
    event_id = response['event_id']

    if event_id == '':
        event_getted = EventsFinder.get_default_event()
    else:
        event_getted = EventsFinder.get_from_external_id(event_id)
    
    activity_types_event = []
    for activity_type2 in event_getted.activity_types:
        vue_activity_type_event = {
            "name": activity_type2.name,
            "description": activity_type2.description,
            'external_id': activity_type2.external_id,
            'price': activity_type2.price, 
            'show_in_home': activity_type2.show_in_home, 
            'show_in_schedule': activity_type2.show_in_schedule, 
            'show_in_app': activity_type2.show_in_app,
        }
        activity_types_event.append(vue_activity_type_event)
        
    event_new = {
    "name": event_getted.name,
    "activity_types": activity_types_event, "external_id": event_getted.external_id,
    }
    
    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'event': '',
            'error': error,
            'role': '',
            }),
        )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])

    if event_getted == '':
        error = 'No default event found! Please set a default event in the menu "Events"'
        
        response = make_response(jsonify(
            {'event': '',
            'error': error,
            'role': user.role,
            }),
        )
        return response

    if time > end_time:
        error = "Activity starting time after ending time"

        response = make_response(jsonify(
            {'event': event_new,
            'error': error,
            'role': user.role,
            }),
        )
        return response

    if points == '':
        points = 0

    # if chat == '':
    #     chat = 'none'
    chat = ""
    if chat == '':
        chat = 'none'

    print(activity_type)
        
    activity = ActivitiesHandler.create_activity(
        chat_enabled=Config.ROCKET_CHAT_ENABLE,
        name=name,
        description=description,
        activity_type=activity_type,
        event=event_getted,
        location=location,
        day=day,
        time=time,
        end_time=end_time,
        registration_link=registration_link,
        registration_open=registration_open,
        points=points,
        quest=False,
        zoom_link="",
        reward_id=reward_id,
        # chat_type=ActivityChatEnum["1"],
        # chat=(chat == "general"),


        volunteers_id = volunteers_to_send
    )
    

    if activity == '':
        companies = CompaniesFinder.get_all()
        speakers = SpeakersFinder.get_all()
        tags = TagsFinder.get_all()
        rewards = RewardsFinder.get_all_rewards()

        try:
            minDate = datetime.strptime(event_getted.start_date, "%d %b %Y, %a").strftime(
                "%Y,%m,%d"
            )
            maxDate = datetime.strptime(event_getted.end_date, "%d %b %Y, %a").strftime(
                "%Y,%m,%d"
            )
        except:
            minDate = ''
            maxDate = ''

        response = make_response(jsonify(
            {'companies': companies,
            'speakers': speakers,
            'tags': tags,
            'rewards': rewards,
            'minDate': minDate,
            'maxDate': maxDate,
            'event': event_new,
            'error': "Failed to create activity! Maybe it already exists :)"}),
        )
        return response

    # extract company names and speaker names from parameters
    
    companies_external_id_response = response["companies_external_id"]
    companies = []
    companies_external_id = []
    for company in companies_external_id_response:

        companies_external_id.append(company["external_id"])
      
    for i in range(len(companies_external_id)):
        companies.append(CompaniesFinder.get_from_external_id(companies_external_id[i]))
    
    speakers_external_id = response["speakers_external_id"]
    speakers = []
    for i in range(len(speakers_external_id)):    
        speakers.append(SpeakersFinder.get_from_external_id(speakers_external_id[i]))
        
    tags_external_id = response["tags_external_id"]
    tags = []
    for i in range(len(tags_external_id)):    
        tags.append(TagsFinder.get_from_external_id(tags_external_id[i]))

    # if company names where provided
    if companies:
        for company in companies:
            if company == '':
                error = "Couldn't find company"
                response = make_response(jsonify(
                    {'event': event_new,
                    'error': error,
                    'role': user.role,
                    }),
                )
                return response
            company_activity = ActivitiesHandler.add_company_activity(
                Config.ROCKET_CHAT_ENABLE, company, activity
            )
            if company_activity == '':
                error = "Failed to create company activity"
                response = make_response(jsonify(
                    {'event': event_new,
                    'error': error,
                    'role': user.role,
                    }),
                )
                return response

    if speakers:
        for name in speakers:
            speaker = SpeakersFinder.get_from_name(name.name)
            if speaker == '':
                response = make_response(jsonify(
                    {'event': event_new,
                    'error': "Couldnt find speaker",
                    'role': user.role,
                    }),
                )
                return response

            speaker_activity = ActivitiesHandler.add_speaker_activity(speaker, activity)
            if speaker_activity == '':
                response = make_response(jsonify(
                    {'event': event_new,
                    'error': "Failed to create speaker activity",
                    'role': user.role,
                    }),
                )
                return response

        if moderator and moderator in speakers:
            moderator = SpeakersFinder.get_from_name(moderator.name)
            if moderator == '':
                response = make_response(jsonify(
                    {'event': event_new,
                    'error': "Couldnt find moderator",
                    'role': user.role,
                    }),
                )
                return response

            ActivitiesHandler.update_activity(
                Config.ROCKET_CHAT_ENABLE,
                activity,
                activity_type,
                moderator_id=moderator.id,
            )

    if tags:
        for name in tags:
            tag = TagsFinder.get_by_name(name.name)
            if tag == '':
                response = make_response(jsonify(
                    {'event': event_new,
                    'error': "Couldnt find tag",
                    'role': user.role,
                    }),
                )
                return response
            

            activity_tag = TagsHandler.add_activity_tag(activity, tag)
            if activity_tag == '':
                response = make_response(jsonify(
                    {'event': event_new,
                    'error': "Failed to create activity tag",
                    'role': user.role,
                    }),
                )
                return response

    
    response = make_response(jsonify(
        {'event': event_new,
        'error': '',
        'role': user.role,
        }),
    )
    return response

# @allowed_roles(["admin", "activities_admin"])
@bp.post("/activity_vue")
@requires_client_auth
def get_activity_vue():
    response = json.loads(request.data.decode('utf-8'))
    activity_external_id = response['activity_external_id']
    
    activity = ActivitiesFinder.get_from_external_id(activity_external_id)
    companies = CompaniesFinder.get_all()
    speakers = SpeakersFinder.get_all()
    tags = TagsFinder.get_all()
    rewards = RewardsFinder.get_all_rewards()

    event = EventsFinder.get_from_parameters({"default": True})
    
    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'event': '',
            'error': error,
            'role': '',
            }),
        )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])
    
    if event == '' or len(event) == 0:
        error = 'No default event found! Please set a default event in the menu "Events"'
        
        response = make_response(jsonify(
            {'event': error,
            'error': error,
            'role': user.role,
            }),
        )
        return response

    activity_types = event[0].activity_types
    company_activities = ActivitiesFinder.get_company_activities_from_activity_id(
        activity_external_id
    )
    speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(
        activity_external_id
    )
    activity_tags = TagsFinder.get_activity_tags_from_activity_id(
        activity_external_id
    )

    try:
        minDate = datetime.strptime(event[0].start_date, "%d %b %Y, %a").strftime(
            "%Y,%m,%d"
        )
        maxDate = datetime.strptime(event[0].end_date, "%d %b %Y, %a").strftime(
            "%Y,%m,%d"
        )
    except:
        minDate = ''
        maxDate = ''
    
    activity_companies = []
    ac_companies = CompaniesFinder.get_from_activity(activity=activity)
    for company in ac_companies:
        activity_companies.append({"name":company.name,"external_id":company.external_id})
    # activity
    
    activity_type_vue = {
        "name": activity.activity_type.name,
        "description": activity.activity_type.description,
        'external_id': activity.activity_type.external_id,
        'price': activity.activity_type.price, 
        'show_in_home': activity.activity_type.show_in_home, 
        'show_in_schedule': activity.activity_type.show_in_schedule, 
        'show_in_app': activity.activity_type.show_in_app,
    }
    reward_id = activity.reward_id
    moderator_id = activity.moderator_id
    
    if activity.chat_type != None:
        chat_type = activity.chat_type.name
    else:
        chat_type = ''
    
    volunteers_selected = []
    for id in activity.volunteers_id:
        vol = UsersFinder.get_by_user_id(id=id)
        volunteers_selected.append( {"name":vol.name, "id":vol.id})

    vue_activity = {
    'name': activity.name,
    "id": activity.id,
    "description": activity.description,
    "day": activity.day,
    "time": activity.time,
    "end_time": activity.end_time,
    "location": activity.location,
    "points": activity.points,
    "activity_type": activity_type_vue,
    'reward_id': reward_id,
    'moderator_id': moderator_id,
    'external_id': activity.external_id,
    'volunteers': volunteers_selected,
    'companies': activity_companies,
    'registration_link': activity.registration_link,
    'registration_open': activity.registration_open, 
    }
 
    volunteers = UsersFinder.get_all_users_by_role("team")

    vue_volunteers=[]

    for volunteer in volunteers:
        vue_volunteer = {
            'name':volunteer.name,
            'id':volunteer.id
        }
        vue_volunteers.append(vue_volunteer)
    # activity_types
    activity_types_vue = []
    for at in activity_types: 
        at_vue = {
            "name": at.name,
            "description": at.description,
            'external_id': at.external_id,
            'price': at.price, 
            'show_in_home': at.show_in_home, 
            'show_in_schedule': at.show_in_schedule, 
            'show_in_app': at.show_in_app,
        }
        activity_types_vue.append(at_vue)
        
    vue_companies = []
    for comp in companies:
        vue_companies.append({"name": comp.name, "external_id": comp.external_id})
    
    vue_speakers = []
    for sp in speakers:
        vue_speakers.append({"name": sp.name, "external_id": sp.external_id})
    
    vue_tags = []
    for tg in tags:
        vue_tags.append({"name": tg.name, "external_id": tg.external_id})
    
    vue_rewards = []
    for rw in rewards:
        vue_rewards.append({"name": rw.name, "external_id": rw.external_id})
    
    reward_external_id=''

    if(reward_id!=None):
        reward_vue = RewardsFinder.get_reward_from_id(reward_id)
        reward_external_id = reward_vue.external_id
    
    moderator_vue = SpeakersFinder.get_speaker_from_id(moderator_id)
    if moderator_vue != None:
        moderator_external_id = moderator_vue.external_id
    else:
        moderator_external_id = ''
       
    companies_external_id = [] 
    for company in company_activities:
        company_vue = CompaniesFinder.get_from_id(company.company_id)
        companies_external_id.append(company_vue.external_id)
   
    
    speakers_external_id = [] 
    for speaker in speaker_activities:
        speaker_vue = SpeakersFinder.get_speaker_from_id(speaker.speaker_id)
        speakers_external_id.append(speaker_vue.external_id)
        
    tags_external_id = [] 
    for tag in activity_tags:
        tag_vue = TagsFinder.get_from_id(tag.tag_id)
        tags_external_id.append(tag_vue.external_id)
    
    
        
    response = make_response(jsonify(
        {'activity': vue_activity,
        'activity_types': activity_types_vue,
        'companies': vue_companies,
        'speakers': vue_speakers,
        'tags': vue_tags,
        'rewards': vue_rewards,
        'companies_external_id': companies_external_id,
        'speakers_external_id': speakers_external_id,
        'tags_external_id': tags_external_id,
        'moderator_external_id': moderator_external_id,
        'reward_external_id': reward_external_id,
        'minDate': minDate,
        'maxDate': maxDate,
        'activity_type_external_id': activity_type_vue['external_id'],
        'volunteers': vue_volunteers,
        'error': ''}),
    )
    return response

# @allowed_roles(["admin", "activities_admin"])
@bp.post("/activity/update_vue")
@requires_client_auth
def update_activity_vue():
    response = json.loads(request.data.decode('utf-8'))

    
    
    activity_external_id = response['activity_external_id']

    activity = ActivitiesFinder.get_from_external_id(activity_external_id)
    company_activities = ActivitiesFinder.get_company_activities_from_activity_id(
        activity_external_id
    )
    speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(
        activity_external_id
    )
    activity_tags = TagsFinder.get_activity_tags_from_activity_id(
        activity_external_id
    )

    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'event': '',
            'error': error,
            'role': '',
            }),
        )
        return response
    
    user = UsersFinder.get_user_from_username(response['username'])

    if activity == '':
        response = make_response(jsonify(
            {'event': '',
            'error': "Couldnt find activity",
            'role': user.role,
            }),
        )
        return response

    name = response['name']
    description = response['description']
    location = response['location']
    day = response['day']
    time = response['time']
    end_time = response['end_time']
    points = response['points'] 
    reward_external_id = response['reward_external_id'] 
    volunteers_response = response['volunteers']
    registration_link = response['registration_link']
    registration_open = response['registration_open']
    volunteers = []
    for volunteer in volunteers_response:
        volunteers.append(volunteer["id"])
  

    if reward_external_id != '':
        reward = RewardsFinder.get_reward_from_external_id(reward_external_id)
        if reward:
            reward_id = reward.id
        else:
            reward_id = None
    else: 
        reward_id = None

    moderator_external_id = response['moderator_external_id'] 
    if moderator_external_id != '':
        moderator = SpeakersFinder.get_from_external_id(moderator_external_id)
    else: 
        moderator = ''
    if time > end_time == '':
        response = make_response(jsonify(
            {'event': '',
            'error': "Activity starting time after ending time",
            'role': user.role,
            }),
        )
        return response


    activity_type_external_id = response['activity_type_external_id']
    activity_type = ActivityTypesFinder.get_from_external_id(activity_type_external_id)

    if points == '':
        points = 0
    
    if registration_open == "true":
        registration_open = True
    else:
        registration_open = False
    
    updated_activity = ActivitiesHandler.update_activity(
        chat_enabled=Config.ROCKET_CHAT_ENABLE,
        activity=activity,
        activity_type=activity_type,
        name=name,
        description=description,
        location=location,
        day=day,
        quest = False,
        time=time,
        end_time=end_time,
        points=points,
        reward_id=reward_id,
        volunteers_id = volunteers,
        registration_link = registration_link,
        registration_open = registration_open
    )

    if company_activities:
        for company_activity in company_activities:
            ActivitiesHandler.delete_company_activities(company_activity)

    if speaker_activities:
        for speaker_activity in speaker_activities:
            ActivitiesHandler.delete_speaker_activities(speaker_activity)

    if activity_tags:
        for activity_tag in activity_tags:
            TagsHandler.delete_activity_tag(activity_tag)

    # extract company names and speaker names from parameters
    companies_external_id_response = response["companies_external_id"]
    companies_external_id = []

    for company in companies_external_id_response:
        companies_external_id.append(company)

    companies = []
    for i in range(len(companies_external_id)):
        companies.append(CompaniesFinder.get_from_external_id(companies_external_id[i]))
    
    speakers_external_id = response["speakers_external_id"]
    speakers = []
    for i in range(len(speakers_external_id)):    
        speakers.append(SpeakersFinder.get_from_external_id(speakers_external_id[i]))
        
    tags_external_id = response["tags_external_id"]
    tags = []
    for i in range(len(tags_external_id)):    
        tags.append(TagsFinder.get_from_external_id(tags_external_id[i]))


    # if company names where provided
    if companies:
        for index, name in enumerate(companies):
            company = CompaniesFinder.get_from_name(name.name)
            if company == '':
                response = make_response(jsonify(
                    {'event': '',
                    'error': "Couldnt find company",
                    'role': user.role,
                    }),
                )
                return response

            company_activity = ActivitiesHandler.add_company_activity(
                Config.ROCKET_CHAT_ENABLE, company, activity
            )
            if company_activity == '':
                response = make_response(jsonify(
                    {'event': '',
                    'error': "Failed to create company activity",
                    'role': user.role,
                    }),
                )
                return response

    if speakers:
        for name in speakers:
            speaker = SpeakersFinder.get_from_name(name.name)
            if speaker == '':
                response = make_response(jsonify(
                    {'event': '',
                    'error': "Couldnt find speaker",
                    'role': user.role,
                    }),
                )
                return response

            speaker_activity = ActivitiesHandler.add_speaker_activity(speaker, activity)
            if speaker_activity == '':
                response = make_response(jsonify(
                    {'event': '',
                    'error': "Failed to create speaker activity",
                    'role': user.role,
                    }),
                )
                return response

        if moderator and moderator in speakers:
            moderator = SpeakersFinder.get_from_name(moderator.name)
            if moderator == '':
                response = make_response(jsonify(
                    {'event': '',
                    'error': "Couldnt find moderator",
                    'role': user.role,
                    }),
                )
                return response

            ActivitiesHandler.update_activity(
                Config.ROCKET_CHAT_ENABLE,
                activity,
                activity_type,
                moderator_id=moderator.id,
            )

        elif not moderator:
            ActivitiesHandler.update_activity(
                Config.ROCKET_CHAT_ENABLE, activity, activity_type, moderator_id=None
            )

    if tags:
        for name in tags:
            tag = TagsFinder.get_by_name(name.name)
            if tag == '':
                response = make_response(jsonify(
                    {'event': '',
                    'error': "Couldnt find tag",
                    'role': user.role,
                    }),
                )
                return response

            activity_tag = TagsHandler.add_activity_tag(activity, tag)
            if activity_tag == '':
                response = make_response(jsonify(
                    {'event': '',
                    'error': "Failed to create activity tag",
                    'role': user.role,
                    }),
                )
                return response

    if updated_activity == '':
        event = EventsFinder.get_from_parameters({"default": True})

        if event == '' or len(event) == 0:
            error = 'No default event found! Please set a default event in the menu "Events"'
            
            response = make_response(jsonify(
                {'event': '',
                'error': error,
                'role': user.role,
                }),
            )
            return response

        activity_types = event[0].activity_types

        try:
            minDate = datetime.strptime(event[0].start_date, "%d %b %Y, %a").strftime(
                "%Y,%m,%d"
            )
            maxDate = datetime.strptime(event[0].end_date, "%d %b %Y, %a").strftime(
                "%Y,%m,%d"
            )
        except:
            minDate = ''
            maxDate = ''

        response = make_response(jsonify(
            {'activity': activity,
            'types': activity_types,
            'companies': CompaniesFinder.get_all(),
            'speakers': SpeakersFinder.get_all(),
            'tags': TagsFinder.get_all(),
            'rewards': RewardsFinder.get_all_rewards(),
            'minDate': minDate,
            'maxDate': maxDate,
            'error': "Failed to update activity!"}),
        )
        return response

    response = make_response(jsonify(
        {'event': '',
        'error': '',
        'role': user.role,
        }),
    )
    return response

# @allowed_roles(["admin", "activities_admin"])
@bp.post("/activity/delete_vue")
@requires_client_auth
def delete_activity_vue():
    response = json.loads(request.data.decode('utf-8'))
    activity_external_id = response['activity_external_id']

    activity = ActivitiesFinder.get_from_external_id(activity_external_id)
    
        
    if ActivitiesHandler.delete_activity(Config.ROCKET_CHAT_ENABLE, activity):
        return '',204
    
    return "Failed to delete activity",204

# @allowed_roles(["admin", "activities_admin"])
@bp.post("/activity/code_vue")
@requires_client_auth
def generate_codes_vue():
    response = json.loads(request.data.decode('utf-8'))
    
    activity_external_id = response['activity_external_id']
    
    activity = ActivitiesFinder.get_from_external_id(activity_external_id)
    
    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'error': error}),
        )
        return jsonify('') # response
    
    user = UsersFinder.get_user_from_username(response['username'])

    #if user.role != 'admin' and user.role != 'activities_admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #        {'error': error}),
    #    )
    #    return jsonify('') # response
    
    if activity == '':
        error = "Couldnt find activity"
        return jsonify('') # response

    number = response['number']
    
    if number == '':
        number = 1
    
    activity_codes = []

    code = response['code'] 
    if code is not None and len(code) == 19:
        code = code.replace("-","")
    else:
        code = ''

    for _ in range(int(number)):
        activity_codes.append(
            ActivityCodesHandler.create_activity_code(code=code, activity_id=activity.id).code
        )

    return jsonify(activity_codes)

# @allowed_roles(["admin", "activities_admin"])
@bp.post("/activity/codes-delete_vue")
@requires_client_auth
def delete_activity_code_vue():
    response = json.loads(request.data.decode('utf-8'))
    
    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'error': error}),
        )
        return jsonify('') # response
    
    user = UsersFinder.get_user_from_username(response['username'])

    #if user.role != 'admin' and user.role != 'activities_admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #        {'error': error}),
    #    )
    #    return jsonify('') # response
    
    activity_external_id = response['activity_external_id']
    
    activity = ActivitiesFinder.get_from_external_id(activity_external_id)
    if activity == '':
        return jsonify("Couldnt find activity")

    codes = ActivityCodesFinder.get_from_parameters({"activity_id": activity.id})
    for code in codes:
        if not ActivityCodesHandler.delete_activity_code(code):
            return jsonify("Failed"), 500

    return jsonify("Success")

# @allowed_roles(["admin", "activities_admin"])
@bp.post("/code/delete_vue")
@requires_client_auth
def delete_code_vue():
    response = json.loads(request.data.decode('utf-8'))
    
    if response['username'] == "":
        error = 'You need to log in'
        response = make_response(jsonify(
            {'error': error}),
        )
        return jsonify('') # response
    
    user = UsersFinder.get_user_from_username(response['username'])

    #if user.role != 'admin' and user.role != 'activities_admin':
    #    error = 'ACCESS DENIED'
    #    response = make_response(jsonify(
    #        {'error': error}),
    #    )
    #    return jsonify('') # response
    
    code = response['code']
    code = ActivityCodesFinder.get_from_code(code)
    if code == '' or code == None or code == 'None':
        return jsonify("Couldnt find code")
    return jsonify({"success": ActivityCodesHandler.delete_activity_code(code)})
    
# Activities routes
@bp.get("/activities")
@allow_all_roles
def activities_dashboard():
    search_parameters = request.args
    name = request.args.get("name")

    # get event
    event_id = request.args.get("event", None)

    if event_id is None:
        event = EventsFinder.get_default_event()
    else:
        event = EventsFinder.get_from_external_id(event_id)

    events = EventsFinder.get_all()

    if event is None:
        error = (
            'No default event found! Please set a default event in the menu "Events"'
        )
        return render_template(
            "admin/activities/activities_dashboard.html",
            event=None,
            events=events,
            activities=None,
            error=error,
            search=None,
            role=current_user.role,
        )

    # handle search bar requests
    if name is not None:
        search = name
        activities_list = ActivitiesFinder.search_by_name_and_event(name, event)

    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = "search name"

        if "type" in search_parameters:
            type_external_id = search_parameters["type"]
            activity_type = ActivityTypesFinder.get_from_external_id(
                uuid.UUID(type_external_id)
            )
            activities_list = ActivitiesFinder.get_all_from_type_and_event(
                activity_type
            )
        else:
            activities_list = event.activities

    # request endpoint with no parameters should return all activities
    else:
        search = None
        activities_list = event.activities

    if not activities_list:
        error = "No results found"
        return render_template(
            "admin/activities/activities_dashboard.html",
            event=event,
            events=events,
            activities=None,
            error=error,
            search=search,
            role=current_user.role,
        )

    return render_template(
        "admin/activities/activities_dashboard.html",
        event=event,
        events=events,
        activities=activities_list,
        error=None,
        search=search,
        role=current_user.role,
    )


# Activities Types routes
@bp.get("/activities/types")
@allow_all_roles
def activity_types_dashboard():
    events = EventsFinder.get_all()

    event_id = request.args.get("event", None)
    if event_id is None:
        event = EventsFinder.get_default_event()
    else:
        event = EventsFinder.get_from_external_id(event_id)

    if event is None:
        error = (
            'No default event found! Please set a default event in the menu "Events"'
        )
        return render_template(
            "admin/activities/activities_dashboard.html",
            event=None,
            events=events,
            error=error,
            role=current_user.role,
        )

    return render_template(
        "admin/activities/activity_types_dashboard.html",
        event=event,
        events=events,
        error=None,
        role=current_user.role,
    )


@bp.post("/activities/types")
@allow_all_roles
def search_activity_types():
    events = EventsFinder.get_all()

    event = request.form.get("event", None)
    if event is None:
        event = EventsFinder.get_default_event()
    else:
        event = EventsFinder.get_from_external_id(event)

    if event is None:
        error = 'No event found! Please set an event in the menu "Events"'
        return render_template(
            "admin/activities/activities_dashboard.html",
            events=events,
            event=None,
            error=error,
            role=current_user.role,
        )

    return render_template(
        "admin/activities/activity_types_dashboard.html",
        events=events,
        event=event,
        error=None,
        role=current_user.role,
    )


@bp.get("/new-activity-type")
@allowed_roles(["admin", "activities_admin"])
def add_activity_type_dashboard():
    event_id = request.args.get("_event", None)
    event = EventsFinder.get_from_external_id(event_id)
    if event is None:
        return APIErrorValue(
            'No event found! Please set an event in the menu "Events"'
        ).json(500)

    return render_template(
        "admin/activities/add_activity_type.html", event=event, error=None
    )


@bp.post("/new-activity-type")
@allowed_roles(["admin", "activities_admin"])
def create_activity_type():
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")
    show_in_home = request.form.get("show_in_home")
    show_in_schedule = request.form.get("show_in_schedule")
    show_in_app = request.form.get("show_in_app")

    if show_in_home == "True":
        show_in_home = True
    else:
        show_in_home = False

    if show_in_schedule == "True":
        show_in_schedule = True
    else:
        show_in_schedule = False

    if show_in_app == "True":
        show_in_app = True
    else:
        show_in_app = False

    event_id = request.form.get("event_id")
    event = EventsFinder.get_from_external_id(event_id)
    if event is None:
        return APIErrorValue(
            'No event found! Please set an event in the menu "Events"'
        ).json(500)

    activity_type = ActivityTypesHandler.create_activity_type(
        event=event,
        name=name,
        description=description,
        price=price,
        show_in_home=show_in_home,
        show_in_schedule=show_in_schedule,
        show_in_app=show_in_app,
    )

    if activity_type is None:
        return render_template(
            "admin/activities/add_activity_type.html",
            event=event,
            error="Failed to create activity type! Maybe it already exists :)",
        )

    return redirect(url_for("admin_api.activity_types_dashboard"))


@bp.get("/activities/types/<string:activity_type_external_id>")
@allowed_roles(["admin", "activities_admin"])
def get_activity_type(path: ActivityTypePath):
    activity_type = ActivityTypesFinder.get_from_external_id(
        path.activity_type_external_id
    )

    return render_template(
        "admin/activities/update_activity_type.html",
        activity_type=activity_type,
        error=None,
    )


@bp.post("/activities/types/<string:activity_type_external_id>")
@allowed_roles(["admin", "activities_admin"])
def update_activity_type(path: ActivityTypePath):
    name = request.form.get("name")
    description = request.form.get("description")
    price = request.form.get("price")
    show_in_home = request.form.get("show_in_home")
    show_in_schedule = request.form.get("show_in_schedule")
    show_in_app = request.form.get("show_in_app")

    if show_in_home == "True":
        show_in_home = True
    else:
        show_in_home = False

    if show_in_schedule == "True":
        show_in_schedule = True
    else:
        show_in_schedule = False

    if show_in_app == "True":
        show_in_app = True
    else:
        show_in_app = False

    activity_type = ActivityTypesFinder.get_from_external_id(
        path.activity_type_external_id
    )

    updated_activity_type = ActivityTypesHandler.update_activity_type(
        activity_type=activity_type,
        name=name,
        description=description,
        price=price,
        show_in_home=show_in_home,
        show_in_schedule=show_in_schedule,
        show_in_app=show_in_app,
    )

    if updated_activity_type is None:
        return render_template(
            "admin/activities/update_activity_type.html",
            activity_type=activity_type,
            error="Failed to update activity type!",
        )

    return redirect(url_for("admin_api.activity_types_dashboard"))


@bp.get("/activities/types/<string:activity_type_external_id>/delete")
@allowed_roles(["admin", "activities_admin"])
def delete_activity_type(path: ActivityTypePath):
    activity_type = ActivityTypesFinder.get_from_external_id(
        path.activity_type_external_id
    )

    if activity_type.activities:
        for activity in activity_type.activities:
            if activity is None:
                return APIErrorValue("Couldnt find activity").json(500)

            company_activities = (
                ActivitiesFinder.get_company_activities_from_activity_id(
                    activity.external_id
                )
            )
            speaker_activities = (
                ActivitiesFinder.get_speaker_activities_from_activity_id(
                    activity.external_id
                )
            )

            if company_activities:
                for company_activity in company_activities:
                    ActivitiesHandler.delete_company_activities(company_activity)

            if speaker_activities:
                for speaker_activity in speaker_activities:
                    ActivitiesHandler.delete_speaker_activities(speaker_activity)

            if not ActivitiesHandler.delete_activity(
                Config.ROCKET_CHAT_ENABLE, activity
            ):
                return APIErrorValue("Couldnt delete activity").json(500)

    if ActivityTypesHandler.delete_activity_type(activity_type):
        return redirect(url_for("admin_api.activity_types_dashboard"))

    return render_template(
        "admin/activities/update_activity_type.html",
        activity_type=activity_type,
        error="Failed to update activity type!",
    )


@bp.get("/new-activity")
@allowed_roles(["admin", "activities_admin"])
def add_activity_dashboard():
    companies = CompaniesFinder.get_all()
    speakers = SpeakersFinder.get_all()
    tags = TagsFinder.get_all()
    rewards = RewardsFinder.get_all_rewards()

    event_id = request.args.get("event", None)
    if event_id is None:
        event = EventsFinder.get_default_event()
    else:
        event = EventsFinder.get_from_external_id(event_id)

    if event is None:
        error = (
            'No default event found! Please set a default event in the menu "Events"'
        )
        return render_template(
            "admin/activities/activities_dashboard.html",
            event=None,
            error=error,
            role=current_user.role,
        )

    try:
        minDate = datetime.strptime(event.start_date, "%d %b %Y, %a").strftime(
            "%Y,%m,%d"
        )
        maxDate = datetime.strptime(event.end_date, "%d %b %Y, %a").strftime("%Y,%m,%d")
    except:
        minDate = None
        maxDate = None

    return render_template(
        "admin/activities/add_activity.html",
        companies=companies,
        speakers=speakers,
        tags=tags,
        minDate=minDate,
        maxDate=maxDate,
        event=event,
        rewards=rewards,
        code_workflows=CodeFlowEnum,
        error=None,
    )


@bp.post("/new-activity")
@allowed_roles(["admin", "activities_admin"])
def create_activity():
    name = request.form.get("name")
    description = request.form.get("description")
    location = request.form.get("location")
    day = request.form.get("day")
    time = request.form.get("time")
    end_time = request.form.get("end_time")
    registration_link = request.form.get("registration_link")
    registration_open = request.form.get("registration_open")
    points = request.form.get("points") or None
    quest = request.form.get("quest")
    chat = request.form.get("chat")
    zoom_link = request.form.get("zoom_url")
    reward_id = request.form.get("reward") or None
    moderator = request.form.get("moderator") or None
    code_work_flow = request.form.get("code_work_flow")
    code_per_company = request.form.get("code_per_company")

    if registration_open == "True":
        registration_open = True
    else:
        registration_open = False

    if quest == "True":
        quest = True
    else:
        quest = False

    if code_per_company == "True":
        code_per_company = True
    else:
        code_per_company = False

    activity_type_external_id = request.form.get("type")
    activity_type = ActivityTypesFinder.get_from_external_id(
        uuid.UUID(activity_type_external_id)
    )
    event = activity_type.event

    if event is None:
        error = (
            'No default event found! Please set a default event in the menu "Events"'
        )
        return render_template(
            "admin/activities/activities_dashboard.html",
            event=None,
            error=error,
            role=current_user.role,
        )

    if time > end_time:
        error = "Activity starting time after ending time"
        return render_template(
            "admin/activities/activities_dashboard.html",
            event=event,
            error=error,
            role=current_user.role,
        )

    activity = ActivitiesHandler.create_activity(
        chat_enabled=Config.ROCKET_CHAT_ENABLE,
        name=name,
        description=description,
        activity_type=activity_type,
        event=event,
        location=location,
        day=day,
        time=time,
        end_time=end_time,
        registration_link=registration_link,
        registration_open=registration_open,
        points=points,
        quest=quest,
        zoom_link=zoom_link,
        chat_type=ActivityChatEnum[chat],
        chat=(chat == "general"),
        reward_id=reward_id,
        code_work_flow=CodeFlowEnum(code_work_flow),
        code_per_company=code_per_company,
    )

    if activity is None:
        companies = CompaniesFinder.get_all()
        speakers = SpeakersFinder.get_all()
        tags = TagsFinder.get_all()
        rewards = RewardsFinder.get_all_rewards()

        try:
            minDate = datetime.strptime(event.start_date, "%d %b %Y, %a").strftime(
                "%Y,%m,%d"
            )
            maxDate = datetime.strptime(event.end_date, "%d %b %Y, %a").strftime(
                "%Y,%m,%d"
            )
        except:
            minDate = None
            maxDate = None

        return render_template(
            "admin/activities/add_activity.html",
            companies=companies,
            speakers=speakers,
            tags=tags,
            rewards=rewards,
            minDate=minDate,
            maxDate=maxDate,
            event=event,
            error="Failed to create activity! Maybe it already exists :)",
        )

    # extract company names and speaker names from parameters
    companies = request.form.getlist("company")
    speakers = request.form.getlist("speaker")
    tags = request.form.getlist("tag")

    # if company names where provided
    if companies:
        for index, name in enumerate(companies):
            company = CompaniesFinder.get_from_name(name)
            if company is None:
                return APIErrorValue("Couldnt find company").json(500)

            company_activity = ActivitiesHandler.add_company_activity(
                Config.ROCKET_CHAT_ENABLE, company, activity
            )
            if company_activity is None:
                return APIErrorValue("Failed to create company activity").json(500)

    if speakers:
        for name in speakers:
            speaker = SpeakersFinder.get_from_name(name)
            if speaker is None:
                return APIErrorValue("Couldnt find speaker").json(500)

            speaker_activity = ActivitiesHandler.add_speaker_activity(speaker, activity)
            if speaker_activity is None:
                return APIErrorValue("Failed to create speaker activity").json(500)

        if moderator and moderator in speakers:
            moderator = SpeakersFinder.get_from_name(moderator)
            if moderator is None:
                return APIErrorValue("Couldnt find moderator").json(500)

            ActivitiesHandler.update_activity(
                Config.ROCKET_CHAT_ENABLE,
                activity,
                activity_type,
                moderator_id=moderator.id,
            )

    if tags:
        for name in tags:
            tag = TagsFinder.get_by_name(name)
            if tag is None:
                return APIErrorValue("Couldnt find tag").json(500)

            activity_tag = TagsHandler.add_activity_tag(activity, tag)
            if activity_tag is None:
                return APIErrorValue("Failed to create activity tag").json(500)

    return redirect(url_for("admin_api.activities_dashboard"))


@bp.get("/activity/<string:activity_external_id>")
@allowed_roles(["admin", "activities_admin"])
def get_activity(path: ActivityPath):
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    companies = CompaniesFinder.get_all()
    speakers = SpeakersFinder.get_all()
    tags = TagsFinder.get_all()
    rewards = RewardsFinder.get_all_rewards()

    event = EventsFinder.get_from_parameters({"default": True})
    if event is None or len(event) == 0:
        error = (
            'No default event found! Please set a default event in the menu "Events"'
        )
        return render_template(
            "admin/activities/activities_dashboard.html",
            event=None,
            error=error,
            role=current_user.role,
        )

    activity_types = event[0].activity_types
    company_activities = ActivitiesFinder.get_company_activities_from_activity_id(
        path.activity_external_id
    )
    speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(
        path.activity_external_id
    )
    activity_tags = TagsFinder.get_activity_tags_from_activity_id(
        path.activity_external_id
    )

    try:
        minDate = datetime.strptime(event[0].start_date, "%d %b %Y, %a").strftime(
            "%Y,%m,%d"
        )
        maxDate = datetime.strptime(event[0].end_date, "%d %b %Y, %a").strftime(
            "%Y,%m,%d"
        )
    except:
        minDate = None
        maxDate = None

    return render_template(
        "admin/activities/update_activity.html",
        activity=activity,
        activity_types=activity_types,
        companies=companies,
        speakers=speakers,
        tags=tags,
        rewards=rewards,
        company_activities=[company.company_id for company in company_activities],
        speaker_activities=[speaker.speaker_id for speaker in speaker_activities],
        activity_tags=[tag.tag_id for tag in activity_tags],
        minDate=minDate,
        maxDate=maxDate,
        code_workflows=CodeFlowEnum,
        error=None,
    )


@bp.post("/activity/<string:activity_external_id>")
@allowed_roles(["admin", "activities_admin"])
def update_activity(path: ActivityPath):
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    company_activities = ActivitiesFinder.get_company_activities_from_activity_id(
        path.activity_external_id
    )
    speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(
        path.activity_external_id
    )
    activity_tags = TagsFinder.get_activity_tags_from_activity_id(
        path.activity_external_id
    )

    if activity is None:
        return APIErrorValue("Couldnt find activity").json(500)

    name = request.form.get("name")
    description = request.form.get("description")
    location = request.form.get("location")
    day = request.form.get("day")
    time = request.form.get("time")
    end_time = request.form.get("end_time")
    registration_link = request.form.get("registration_link")
    registration_open = request.form.get("registration_open")
    points = request.form.get("points") or None
    quest = request.form.get("quest")
    chat = request.form.get("chat")
    zoom_link = request.form.get("zoom_url")
    reward_id = request.form.get("reward") or None
    moderator = request.form.get("moderator") or None
    code_work_flow = request.form.get("code_workflow")
    code_per_company = request.form.get("code_per_company")

    if time > end_time is None:
        return APIErrorValue("Activity starting time after ending time").json(500)

    if registration_open == "True":
        registration_open = True
    else:
        registration_open = False

    if quest == "True":
        quest = True
    else:
        quest = False

    if code_per_company == "True":
        code_per_company = True
    else:
        code_per_company = False

    chat_type = ActivityChatEnum[chat] if chat else None

    activity_type_external_id = request.form.get("type")
    activity_type = ActivityTypesFinder.get_from_external_id(
        uuid.UUID(activity_type_external_id)
    )

    updated_activity = ActivitiesHandler.update_activity(
        chat_enabled=Config.ROCKET_CHAT_ENABLE,
        activity=activity,
        activity_type=activity_type,
        name=name,
        description=description,
        location=location,
        day=day,
        time=time,
        end_time=end_time,
        registration_link=registration_link,
        registration_open=registration_open,
        points=points,
        quest=quest,
        zoom_link=zoom_link,
        chat_type=chat_type,
        chat=(chat == "general"),
        reward_id=reward_id,
        code_work_flow=CodeFlowEnum(code_work_flow),
        code_per_company=code_per_company,
    )

    if company_activities:
        for company_activity in company_activities:
            ActivitiesHandler.delete_company_activities(company_activity)

    if speaker_activities:
        for speaker_activity in speaker_activities:
            ActivitiesHandler.delete_speaker_activities(speaker_activity)

    if activity_tags:
        for activity_tag in activity_tags:
            TagsHandler.delete_activity_tag(activity_tag)

    # extract company names and speaker names from parameters
    companies = request.form.getlist("company")
    speakers = request.form.getlist("speaker")
    tags = request.form.getlist("tag")

    # if company names where provided
    if companies:
        for index, name in enumerate(companies):
            company = CompaniesFinder.get_from_name(name)
            if company is None:
                return APIErrorValue("Couldnt find company").json(500)

            company_activity = ActivitiesHandler.add_company_activity(
                Config.ROCKET_CHAT_ENABLE, company, activity
            )
            if company_activity is None:
                return APIErrorValue("Failed to create company activity").json(500)

    if speakers:
        for name in speakers:
            speaker = SpeakersFinder.get_from_name(name)
            if speaker is None:
                return APIErrorValue("Couldnt find speaker").json(500)

            speaker_activity = ActivitiesHandler.add_speaker_activity(speaker, activity)
            if speaker_activity is None:
                return APIErrorValue("Failed to create speaker activity").json(500)

        if moderator and moderator in speakers:
            moderator = SpeakersFinder.get_from_name(moderator)
            if moderator is None:
                return APIErrorValue("Couldnt find moderator").json(500)

            ActivitiesHandler.update_activity(
                Config.ROCKET_CHAT_ENABLE,
                activity,
                activity_type,
                moderator_id=moderator.id,
            )

        elif not moderator:
            ActivitiesHandler.update_activity(
                Config.ROCKET_CHAT_ENABLE, activity, activity_type, moderator_id=None
            )

    if tags:
        for name in tags:
            tag = TagsFinder.get_by_name(name)
            if tag is None:
                return APIErrorValue("Couldnt find tag").json(500)

            activity_tag = TagsHandler.add_activity_tag(activity, tag)
            if activity_tag is None:
                return APIErrorValue("Failed to create activity tag").json(500)

    if updated_activity is None:
        event = EventsFinder.get_from_parameters({"default": True})

        if event is None or len(event) == 0:
            error = 'No default event found! Please set a default event in the menu "Events"'
            return render_template(
                "admin/activities/activities_dashboard.html",
                event=None,
                error=error,
                role=current_user.role,
            )

        activity_types = event[0].activity_types

        try:
            minDate = datetime.strptime(event[0].start_date, "%d %b %Y, %a").strftime(
                "%Y,%m,%d"
            )
            maxDate = datetime.strptime(event[0].end_date, "%d %b %Y, %a").strftime(
                "%Y,%m,%d"
            )
        except:
            minDate = None
            maxDate = None

        return render_template(
            "admin/activities/update_activity.html",
            activity=activity,
            types=activity_types,
            companies=CompaniesFinder.get_all(),
            speakers=SpeakersFinder.get_all(),
            tags=TagsFinder.get_all(),
            rewards=RewardsFinder.get_all_rewards(),
            minDate=minDate,
            maxDate=maxDate,
            code_workflows=CodeFlowEnum,
            error="Failed to update activity!",
        )

    return redirect(url_for("admin_api.activities_dashboard"))


@bp.get("/activity/<string:activity_external_id>/delete")
@allowed_roles(["admin", "activities_admin"])
def delete_activity(path: ActivityPath):
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    company_activities = ActivitiesFinder.get_company_activities_from_activity_id(
        path.activity_external_id
    )
    speaker_activities = ActivitiesFinder.get_speaker_activities_from_activity_id(
        path.activity_external_id
    )
    activity_tags = TagsFinder.get_activity_tags_from_activity_id(
        path.activity_external_id
    )

    if activity is None:
        return APIErrorValue("Couldnt find activity").json(500)

    if company_activities:
        for company_activity in company_activities:
            ActivitiesHandler.delete_company_activities(company_activity)

    if speaker_activities:
        for speaker_activity in speaker_activities:
            ActivitiesHandler.delete_speaker_activities(speaker_activity)

    if activity_tags:
        for activity_tag in activity_tags:
            TagsHandler.delete_activity_tag(activity_tag)

    if ActivitiesHandler.delete_activity(Config.ROCKET_CHAT_ENABLE, activity):
        return redirect(url_for("admin_api.activities_dashboard"))

    else:
        return render_template(
            "admin/activities/update_activity.html",
            activity=activity,
            error="Failed to delete activity!",
        )


@bp.post("/activity/<string:activity_external_id>/code")
@allowed_roles(["admin", "activities_admin"])
def generate_codes(path: ActivityPath):
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    if activity is None:
        return APIErrorValue("Couldnt find activity").json(404)

    number = request.form.get("number", 1)
    activity_codes = []

    code = request.form.get("code", None)
    if code is not None and len(code) == 19:
        code = code.replace("-","")
    else:
        code = None

    for _ in range(int(number)):
        activity_codes.append(
            ActivityCodesHandler.create_activity_code(code=code, activity_id=activity.id).code
        )

    return jsonify(activity_codes)


@bp.post("/activity/<string:activity_external_id>/codes-delete")
@allowed_roles(["admin", "activities_admin"])
def delete_activity_code(path: ActivityPath):
    activity = ActivitiesFinder.get_from_external_id(path.activity_external_id)
    if activity is None:
        return APIErrorValue("Couldnt find activity").json(404)

    codes = ActivityCodesFinder.get_from_parameters({"activity_id": activity.id})
    for code in codes:
        if not ActivityCodesHandler.delete_activity_code(code):
            return jsonify("Failed"), 500

    return jsonify("Success")


@bp.post("/code/<string:code>/delete")
@allowed_roles(["admin", "activities_admin"])
def delete_code(path: CodePath):
    code = ActivityCodesFinder.get_from_code(path.code)
    if code is None:
        return APIErrorValue("Couldnt find code").json(404)

    return jsonify({"success": ActivityCodesHandler.delete_activity_code(code)})

@bp.post("/activity/all_activities")
def send_all_activities():
    activities = ActivitiesFinder.get_all()
    activities_to_send = []

    for activity in activities:
        if activity.reward is not None:
            reward_name = activity.reward.name
        else:
            reward_name = ""

        activities_to_send.append({"name":activity.name,"reward":reward_name,"attributed":activity.prize_attributed,"winner":activity.winner, "external_id":activity.external_id}) 
    
    response = make_response(jsonify({
        "activities":activities_to_send,
        "length": len(activities_to_send),
        "error":""
    }))
    return response

@bp.post("/activity/update_attributed")
def update_attributed():
    response = json.loads(request.data.decode('utf-8'))
    activity_external_id = response["external_id"]
    activity = ActivitiesFinder.get_from_external_id(external_id=activity_external_id)
    activity_type = ActivityTypesFinder.get_from_activity_type_id(activity_type_id=activity.activity_type_id)
    students_participated = StudentsFinder.get_students_from_activity_id(activity_id=activity.id)
    activities = ActivitiesFinder.get_all()
    activities_to_send = []
    if students_participated is not []:
        winner = random.randint(0, len(students_participated)-1)
        student_winner = students_participated[winner]
        StudentRewardsHandler.add_reward_student(student=student_winner.id,reward =  activity.reward.id)
        updated_activity = ActivitiesHandler.update_activity(winner = student_winner.user.name,chat_enabled=False,activity=activity,activity_type=activity_type,prize_attributed = True)
        if(updated_activity):
            response = make_response(jsonify({
                "error":""
        }))
            return response
        
    return make_response(jsonify({
                "error":"Failed to attribute reward"
        }))