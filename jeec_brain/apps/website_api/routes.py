from . import bp
from flask import render_template, current_app, request, redirect, url_for
from copy import deepcopy

# Finders
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.speakers_finder import SpeakersFinder
from jeec_brain.finders.teams_finder import TeamsFinder
from jeec_brain.finders.events_finder import EventsFinder

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
@bp.route('/activities', methods=['GET'])
@requires_client_auth
def get_activities():
    search_parameters = request.args
    name = request.args.get('name')

    # handle search bar requests
    if name is not None:
        search = name
        activities_list = ActivitiesFinder.search_by_name(name)
    
    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = 'search name'

        activities_list = ActivitiesFinder.get_from_parameters(search_parameters)

    # request endpoint with no parameters should return all activities
    else:
        search = None
        activities_list = ActivitiesFinder.get_all()
    
    if activities_list is None or len(activities_list) == 0:
        return APIErrorValue('No results found').json(400)

    return ActivitiesValue(activities_list).json(200)


# Companies routes
@bp.route('/companies', methods=['GET'])
@requires_client_auth
def get_companies():
    search_parameters = request.args
    name = request.args.get('name')

    # handle search bar requests
    if name is not None:
        search = name
        companies_list = CompaniesFinder.get_website_company(name)
    
    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = 'search name'

        companies_list = CompaniesFinder.get_website_companies(search_parameters)

    # request endpoint with no parameters should return all companies
    else:
        search = None
        companies_list = CompaniesFinder.get_all()
    
    if companies_list is None or len(companies_list) == 0:
        return APIErrorValue('No results found').json(400)

    return CompaniesValue(companies_list).json(200)


# Speakers routes
@bp.route('/speakers', methods=['GET'])
@requires_client_auth
def get_speakers():
    search_parameters = request.args.to_dict()
    name = request.args.get('name')

    # handle search bar requests
    if name is not None:
        search = name
        speakers_list = SpeakersFinder.search_by_name(name)
    
    # handle parameter requests
    elif len(search_parameters) != 0:
        search = 'search name'

        if 'spotlight' in search_parameters:
            if search_parameters['spotlight'] == 'True':
                search_parameters['spotlight'] = True
            elif search_parameters['spotlight'] == 'False':
                search_parameters['spotlight'] = False

        speakers_list = SpeakersFinder.get_from_parameters(search_parameters)

    # request endpoint with no parameters should return all speakers
    else:
        search = None
        speakers_list = SpeakersFinder.get_all()
    
    if speakers_list is None or len(speakers_list) == 0:
        return APIErrorValue('No results found').json(400)

    return SpeakersValue(speakers_list).json(200)


# Team routes
@bp.route('/teams', methods=['GET'])
@requires_client_auth
def get_teams():
    search_parameters = request.args
    name = request.args.get('name')

    # handle search bar requests
    if name is not None:
        search = name
        teams_list = TeamsFinder.search_by_name(name)
    
    # handle parameter requests
    elif len(search_parameters) != 0:
        search_parameters = request.args
        search = 'search name'
        teams_list = TeamsFinder.get_from_parameters(search_parameters)

    # request endpoint with no parameters should return all activities
    else:
        search = None
        teams_list = TeamsFinder.get_all()
    
    if teams_list is None or len(teams_list) == 0:
        return APIErrorValue('No results found').json(400)

    teams_list.sort(key=lambda x: x.website_priority, reverse=True)

    return TeamsValue(teams_list).json(200)

@bp.route('/event', methods=['GET'])
@requires_client_auth
def get_event():
    event = EventsFinder.get_default_event()

    return EventsValue(event).json(200)
