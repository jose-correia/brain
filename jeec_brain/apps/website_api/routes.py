from . import bp
from flask import render_template, current_app, request, redirect, url_for
from copy import deepcopy

# Finders
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.speakers_finder import SpeakersFinder
from jeec_brain.finders.teams_finder import TeamsFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.finders.activity_types_finder import ActivityTypesFinder

# Values
from jeec_brain.values.activities_value import ActivitiesValue
from jeec_brain.values.companies_value import CompaniesValue
from jeec_brain.values.speakers_value import SpeakersValue
from jeec_brain.values.teams_value import TeamsValue
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.values.events_value import EventsValue

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
    search_parameters = request.args
    name = request.args.get("name")

    # handle search bar requests
    if name is not None:
        search = name
        teams_list = TeamsFinder.search_by_name(name)

    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = "search name"
        teams_list = TeamsFinder.get_from_parameters(search_parameters)

    # request endpoint with no parameters should return all activities
    else:
        search = None
        event = EventsFinder.get_default_event()
        teams_list = TeamsFinder.get_from_event_id(event.id)

    if teams_list is None or len(teams_list) == 0:
        return APIErrorValue("No results found").json(400)

    teams_list.sort(key=lambda x: x.website_priority, reverse=True)

    return TeamsValue(teams_list).json(200)


@bp.get("/event")
@requires_client_auth
def get_event():
    event = EventsFinder.get_default_event()

    return EventsValue(event).json(200)


def removeDuplicates(listofElements):
    uniqueList = []

    for elem in listofElements:
        if elem not in uniqueList:
            uniqueList.append(elem)

    return uniqueList
