from jeec_brain.handlers.companies_handler import CompaniesHandler
from . import bp
from flask import render_template, current_app, request, redirect, url_for, make_response, jsonify
from copy import deepcopy
from datetime import datetime

# Finders
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.speakers_finder import SpeakersFinder
from jeec_brain.finders.teams_finder import TeamsFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.finders.activity_types_finder import ActivityTypesFinder
from jeec_brain.finders.levels_finder import LevelsFinder
from jeec_brain.finders.rewards_finder import RewardsFinder

# Values
from jeec_brain.values.activities_value import ActivitiesValue
from jeec_brain.values.companies_value import CompaniesValue
from jeec_brain.values.speakers_value import SpeakersValue
from jeec_brain.values.teams_value import TeamsValue
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.values.events_value import EventsValue
from jeec_brain.values.website_rewards_value import WebsiteRewardsValue


# Handlers
from jeec_brain.handlers.events_handler import EventsHandler

from jeec_brain.apps.auth.wrappers import requires_client_auth


# Activities routes
@bp.get("/activities")
@requires_client_auth
def get_activities():
    search_parameters = request.args
    name = request.args.get("name")
    speaker = request.args.get("speaker")
    company = request.args.get("company")

    event = request.args.get("event")
    if event is None:
        event = EventsFinder.get_default_event()
    else:
        event = EventsFinder.get_from_name(event)

    if event is None:
        return APIErrorValue("Event no found!").json(404)

    activities_list = []

    # handle search bar requests
    if name is not None:
        search = name
        activities_list = ActivitiesFinder.search_by_name_and_event(search, event)

    # handle parameter requests
    elif speaker is not None:
        search = speaker
        speaker = SpeakersFinder.get_from_name(search)

        if speaker:
            activities_list = ActivitiesFinder.get_activities_from_speaker_and_event(
                speaker, event
            )

    elif company is not None:
        search = company
        company = CompaniesFinder.get_from_name(search)

        if company:
            activities_list = ActivitiesFinder.get_activities_from_company_and_event(
                company, event
            )

    elif len(search_parameters) != 0:
        search = "search name"

        try:
            search_parameters = request.args.to_dict()
            search_parameters["type"] = ActivityTypesFinder.get_from_name(
                search_parameters["type"]
            ).id
            search_parameters["activity_type_id"] = search_parameters.pop("type")
        except:
            pass

        activities_list = ActivitiesFinder.get_from_parameters(search_parameters)

    # request endpoint with no parameters should return all activities
    else:
        search = None
        activities_list = ActivitiesFinder.get_activities_from_event(event)

    if activities_list is None:
        return APIErrorValue("No results found").json(400)

    return ActivitiesValue(activities_list).json(200)


# Companies routes
@bp.get("/companies")
@requires_client_auth
def get_companies():
    search_parameters = request.args.to_dict()
    search_parameters.pop("event", None)
    event_name = request.args.get("event", None)

    if event_name is None:
        event = EventsFinder.get_default_event()
    else:
        event = EventsFinder.get_from_name(event_name)

    if event is None:
        return APIErrorValue("Event not found!").json(404)

    companies_list = CompaniesFinder.get_website_companies(event, search_parameters)

    if companies_list is None:
        return APIErrorValue("No results found").json(404)

    return CompaniesValue(companies_list, True).json(200)


# Speakers routes
@bp.get("/speakers")
@requires_client_auth
def get_speakers():
    search_parameters = request.args.to_dict()
    search_parameters.pop("event", None)
    if "spotlight" in search_parameters:
        if search_parameters["spotlight"] == "True":
            search_parameters["spotlight"] = True
        elif search_parameters["spotlight"] == "False":
            search_parameters["spotlight"] = False

    event_name = request.args.get("event")
    if event_name is None:
        event = EventsFinder.get_default_event()
    else:
        event = EventsFinder.get_from_name(event_name)

    if event is None:
        return APIErrorValue("Event not found!").json(404)

    speakers_list = SpeakersFinder.get_website_speakers(event, search_parameters)

    if speakers_list is None:
        return APIErrorValue("No results found").json(400)

    return SpeakersValue(speakers_list).json(200)


# Team routes
@bp.get("/teams")
@requires_client_auth
def get_teams():
    # search_parameters = request.args
    # name = request.args.get("name")

    # handle search bar requests
    # if name is not None:
    #     search = name
    #     teams_list = TeamsFinder.search_by_name(name)

    # handle parameter requests
    # elif len(search_parameters) != 0:
    #     search_parameters = request.args
    #     search = "search name"
    #     teams_list = TeamsFinder.get_from_parameters(search_parameters)

    # request endpoint with no parameters should return all activities
    # else:
    event = EventsFinder.get_default_event()
    teams_list = TeamsFinder.get_from_event_id(event.id)

    if teams_list is None or len(teams_list) == 0:
        return APIErrorValue("No results found").json(204)

    teams_list.sort(key=lambda x: x.website_priority, reverse=True)

    return TeamsValue(teams_list).json(200)


# datetime object containing current date and time
@bp.get("/event")
#@requires_client_auth
def get_event():
    
    event = EventsFinder.get_default_event()
    date = event.start_date

    now = datetime.now()
    print(now)

    day_today = now.day
    hours_today = now.hour

    
    if (date[3:5] != '03' or date[6:10] != '2023'):
        time_to_event = '00/00'
    else: 
        time1 = str((int(date[0:2]) - int(day_today) - 1))
        if int(time1) < 10:
            time1 = '0' + time1
        time2 = str((24 - int(hours_today) - 1))
        
        if int(time2) < 10: 
            time2 = '0' + time2
        time_to_event = time1 + '/' + time2
    
    response = EventsValue(event).json(200)
    return response


@bp.get("/prizes")
def get_prizes():
    """Retrieve the prizes for the current event
    <b>Returns:</b>
        PrizesValue: Returns list with the prizes for the current event
    """

    jeecpot_rewards = RewardsFinder.get_all_jeecpot_rewards()
    levels = LevelsFinder.get_all_levels()
    event = EventsFinder.get_default_event()
    squad_rewards = RewardsFinder.get_all_squad_rewards()
    level_reward = activity_reward = daily_squad_reward = None

    for level in levels:
        if level.reward_id is not None:
            level_reward = RewardsFinder.get_reward_from_id(level.reward_id)
            break

    for activity in event.activities:
        if activity.reward_id is not None:
            activity_reward = RewardsFinder.get_reward_from_id(activity.reward_id)
            break

    for squad_reward in squad_rewards:
        if squad_reward.reward_id is not None:
            daily_squad_reward = RewardsFinder.get_reward_from_id(
                squad_reward.reward_id
            )
            break

    return WebsiteRewardsValue(
        jeecpot_rewards[0], level_reward, activity_reward, daily_squad_reward
    ).json(200)

@bp.get('/job-fair')
@requires_client_auth
def get_job_fair_companies():
    event = EventsFinder.get_default_event()
    event_dates = EventsHandler.get_event_dates(event)
    job_fair_type = ActivityTypesFinder.get_from_name('Job Fair')
    job_fairs = ActivitiesFinder.get_all_from_type(job_fair_type)
    companies0 = []
    companies1 = []
    companies2 = []
    companies3 = []
    companies4 = []
    for job_fair in job_fairs:
        company = CompaniesFinder.get_from_activity(job_fair)
        if company:
            company_img = CompaniesHandler.find_image(company[0].name)
        
            if(job_fair.day == event_dates[0]):
                companies0.append(company_img)
            elif (job_fair.day == event_dates[1]):
                companies1.append(company_img)
            elif (job_fair.day == event_dates[2]):
                companies2.append(company_img)
            elif (job_fair.day == event_dates[3]):
                companies3.append(company_img)
            else:
                companies4.append(company_img)


    return jsonify({
        '0':companies0,
        '1':companies1,
        '2':companies2,
        '3':companies3,
        '4':companies4,
    })




def removeDuplicates(listofElements):
    uniqueList = []

    for elem in listofElements:
        if elem not in uniqueList:
            uniqueList.append(elem)

    return uniqueList
