from jeec_brain.apps.companies_api import bp
from flask import Response, send_file, render_template, send_from_directory
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.handlers.file_handler import FileHandler
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.activity_codes_finder import ActivityCodesFinder

from jeec_brain.models.logs import Logs
from jeec_brain.models.users import Users
from jeec_brain.models.students import Students
from jeec_brain.models.activities import Activities
from jeec_brain.models.events import Events
from jeec_brain.models.company_activities import CompanyActivities
from jeec_brain.models.student_activities import StudentActivities
from jeec_brain.database import db_session

from sqlalchemy import or_
from sqlalchemy import func

from datetime import datetime


@bp.get('/statistics')
@require_company_login
def statistics_dashboard(company_user):
    event = EventsFinder.get_default_event()
    company_user = UsersFinder.get_company_user_from_user(current_user)
    interested_students = StudentsFinder.get_company_students(company_user.company)
    company_activities = ActivitiesFinder.get_activities_from_company_and_event(company_user.company, event)
    company = company_user.company

    interactions = db_session.query(Logs) \
                     .join(Activities, Logs.entrypoint.contains(Activities.name)) \
                     .join(Users, Users.username == Logs.user_id) \
                     .join(Students, Users.id == Students.user_id) \
                     .with_entities(Activities.name, Students.course, Students.entry_year, func.count(Activities.name)) \
                     .filter((Events.id == event.id) & (Events.id == Activities.event_id) & (CompanyActivities.activity_id == Activities.id) & (CompanyActivities.company_id == company.id)) \
                     .group_by(Activities.name, Students.course, Students.entry_year) \
                     .all()

    total_interactions = 0
    total_interactions_by_activity = {}
    total_interactions_by_course = {}
    total_interactions_by_year = {}
    interactions_by_course = {}
    interactions_by_year = {}
    for interaction_type in interactions:
        total_interactions += interaction_type[3]

        if "Job Fair" in interaction_type[0]:
            interaction_type = list(interaction_type)
            interaction_type[0] = interaction_type[0].rsplit(" ", 1)[0]
        
        if interaction_type[0] not in total_interactions_by_activity:
            total_interactions_by_activity[interaction_type[0]] = interaction_type[3]

            interactions_by_course[interaction_type[0]] = {}
            interactions_by_course[interaction_type[0]][interaction_type[1]] = interaction_type[3]

            interactions_by_year[interaction_type[0]] = {}
            interactions_by_year[interaction_type[0]][interaction_type[2]] = interaction_type[3]
        else:
            total_interactions_by_activity[interaction_type[0]] += interaction_type[3]

            if interaction_type[1] not in interactions_by_course[interaction_type[0]]:
                interactions_by_course[interaction_type[0]][interaction_type[1]] = interaction_type[3]
            else:
                interactions_by_course[interaction_type[0]][interaction_type[1]] += interaction_type[3]

            if interaction_type[2] not in interactions_by_year[interaction_type[0]]:
                interactions_by_year[interaction_type[0]][interaction_type[2]] = interaction_type[3]
            else:
                interactions_by_year[interaction_type[0]][interaction_type[2]] += interaction_type[3]


        if interaction_type[1] not in total_interactions_by_course:
            total_interactions_by_course[interaction_type[1]] = interaction_type[3]
        else:
            total_interactions_by_course[interaction_type[1]] += interaction_type[3]

        if interaction_type[2] not in total_interactions_by_year:
            total_interactions_by_year[interaction_type[2]] = interaction_type[3]
        else:
            total_interactions_by_year[interaction_type[2]] += interaction_type[3]

    participations = StudentActivities \
        .query \
        .join(Activities, StudentActivities.activity_id == Activities.id) \
        .join(Students, StudentActivities.student_id == Students.id) \
        .with_entities(Activities.name, Students.course, Students.entry_year, func.count(Activities.name), Activities.day) \
        .filter((Events.id == event.id) & (Events.id == Activities.event_id) & (CompanyActivities.activity_id == Activities.id) & (CompanyActivities.company_id == company.id)) \
        .group_by(Activities.name, Students.course, Students.entry_year, Activities.day) \
        .all()

    total_participations = 0
    total_participations_by_activity = {}
    total_participations_by_course = {}
    total_participations_by_year = {}
    participations_by_course = {}
    participations_by_year = {}
    for participation_type in participations:
        total_participations += participation_type[3]

        if "Booth" in participation_type[0]:
            week_day = participation_type[4][-3:]
            participation_type = list(participation_type)
            if week_day == "Mon":
                participation_type[0] = "Job Fair Monday"
            elif week_day == "Tue":
                participation_type[0] = "Job Fair Tuesday"
            elif week_day == "Wed":
                participation_type[0] = "Job Fair Wednesday"
            elif week_day == "Thu":
                participation_type[0] = "Job Fair Thursday"
            elif week_day == "Fri":
                participation_type[0] = "Job Fair Friday"

        if participation_type[0] not in total_participations_by_activity:
            total_participations_by_activity[participation_type[0]] = participation_type[3]

            participations_by_course[participation_type[0]] = {}
            participations_by_course[participation_type[0]][participation_type[1]] = participation_type[3]

            participations_by_year[participation_type[0]] = {}
            participations_by_year[participation_type[0]][participation_type[2]] = participation_type[3]
        else:
            total_participations_by_activity[participation_type[0]] += participation_type[3]

            if participation_type[1] not in participations_by_course[participation_type[0]]:
                participations_by_course[participation_type[0]][participation_type[1]] = participation_type[3]
            else:
                participations_by_course[participation_type[0]][participation_type[1]] += participation_type[3]

            if participation_type[2] not in participations_by_year[participation_type[0]]:
                participations_by_year[participation_type[0]][participation_type[2]] = participation_type[3]
            else:
                participations_by_year[participation_type[0]][participation_type[2]] += participation_type[3]

        if participation_type[1] not in total_participations_by_course:
            total_participations_by_course[participation_type[1]] = participation_type[3]
        else:
            total_participations_by_course[participation_type[1]] += participation_type[3]

        if participation_type[2] not in total_participations_by_year:
            total_participations_by_year[participation_type[2]] = participation_type[3]
        else:
            total_participations_by_year[participation_type[2]] += participation_type[3]

    interactions_by_course["Total"] = total_interactions_by_course;
    interactions_by_year["Total"] = total_interactions_by_year;

    participations_by_course["Total"] = total_participations_by_course;
    participations_by_year["Total"] = total_participations_by_year;

    return render_template('companies/statistics/statistics_dashboard.html', \
                           participations_by_course=participations_by_course, \
                           participations_by_year=participations_by_year, \
                           interactions_by_course=interactions_by_course, \
                           interactions_by_year=interactions_by_year, \
                           total_participations_by_year=total_participations_by_year,\
                           total_participations=total_participations,\
                           total_participations_by_activity=total_participations_by_activity,\
                           total_participations_by_course=total_participations_by_course,\
                           total_interactions_by_year=total_interactions_by_year,\
                           total_interactions=total_interactions,\
                           total_interactions_by_course=total_interactions_by_course,\
                           total_interactions_by_activity=total_interactions_by_activity,\
                           activity="Total",\
                           company_activities=company_activities,\
                           interactions=interactions,\
                           participations=participations,\
                           error=None)
