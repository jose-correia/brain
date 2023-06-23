from typing import Callable, Dict, Tuple, Iterable

import logging

from jeec_brain.apps.companies_api import bp
from flask import Response, send_file, render_template, send_from_directory, jsonify, make_response, request
from flask_login import current_user
from jeec_brain.apps.auth.wrappers import require_company_login
from jeec_brain.handlers.file_handler import FileHandler
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.finders.events_finder import EventsFinder
from jeec_brain.finders.activities_finder import ActivitiesFinder
from jeec_brain.finders.activity_codes_finder import ActivityCodesFinder
from jeec_brain.finders.companies_finder import CompaniesFinder

from jeec_brain.models.logs import Logs
from jeec_brain.models.users import Users
from jeec_brain.models.students import Students
from jeec_brain.models.activities import Activities
from jeec_brain.models.events import Events
from jeec_brain.models.company_activities import CompanyActivities
from jeec_brain.models.student_activities import StudentActivities
from jeec_brain.database import db_session

import json

from jeec_brain.apps.auth.wrappers import requires_client_auth

from sqlalchemy import func

logger = logging.getLogger(__name__)


def get_statistics(query, event, company) -> Iterable[Tuple[str, str, str, int]]:
    return (
        query.with_entities(
            Activities.name,
            Students.course,
            Students.entry_year,
            func.count(Activities.name),
        )
        .filter(
            (Events.id == event.id)
            & (Events.id == Activities.event_id)
            & (CompanyActivities.activity_id == Activities.id)
            & (CompanyActivities.company_id == company.id)
        )
        .group_by(Activities.name, Students.course, Students.entry_year)
        .all()
    )


def get_interactions(db_session) -> Iterable[Tuple[str, str, str, int]]:
    return (
        db_session.query(Logs)
        .join(Activities, Logs.entrypoint.contains(Activities.name))
        .join(Users, Users.username == Logs.user_id)
        .join(Students, Users.id == Students.user_id)
    )


def get_participations(company_id) -> Iterable[Tuple[str, str, str, int]]:
    return (
        StudentActivities.query.join(
            Activities, StudentActivities.activity_id == Activities.id
        )
        .join(Students, StudentActivities.student_id == Students.id)
        .filter(
            (StudentActivities.company_id == -1)
            | (
                (StudentActivities.company_id != None)
                & (StudentActivities.company_id == company_id)
            )
        )
    )


def calc_statistics(
    query_results, group_job_fair: bool
) -> Tuple[int, Dict, Dict, Dict, Dict, Dict]:
    total_count = 0
    total_by_activity = {}
    total_by_course = {}
    total_by_year = {}
    count_by_course = {}
    count_by_year = {}

    for query_result in query_results:
        activity_name, student_course, student_year, interaction_count = query_result

        total_count += interaction_count

        if group_job_fair and "Job Fair" in activity_name:
            activity_name = activity_name.split(" ", 1)[1]

        if activity_name not in total_by_activity:
            total_by_activity[activity_name] = interaction_count

            count_by_course[activity_name] = {}
            count_by_course[activity_name][student_course] = interaction_count

            count_by_year[activity_name] = {}
            count_by_year[activity_name][student_year] = interaction_count
        else:
            total_by_activity[activity_name] += interaction_count

            if student_course not in count_by_course[activity_name]:
                count_by_course[activity_name][student_course] = interaction_count
            else:
                count_by_course[activity_name][student_course] += interaction_count

            if student_year not in count_by_year[activity_name]:
                count_by_year[activity_name][student_year] = interaction_count
            else:
                count_by_year[activity_name][student_year] += interaction_count

        if student_course not in total_by_course:
            total_by_course[student_course] = interaction_count
        else:
            total_by_course[student_course] += interaction_count

        if student_year not in total_by_year:
            total_by_year[student_year] = interaction_count
        else:
            total_by_year[student_year] += interaction_count

    count_by_course["Total"] = total_by_course
    count_by_year["Total"] = total_by_year

    return (
        total_count,
        total_by_activity,
        total_by_course,
        total_by_year,
        count_by_course,
        count_by_year,
    )


def get_data(
    query, event, company, group_job_fair: bool
) -> Tuple[int, Dict, Dict, Dict, Dict, Dict]:
    query_results = get_statistics(query=query, event=event, company=company)

    return calc_statistics(query_results=query_results, group_job_fair=group_job_fair)


@bp.get("/statistics")
@require_company_login
def statistics_dashboard(company_user):
    event = EventsFinder.get_default_event()

    company_user = UsersFinder.get_company_user_from_user(current_user)
    company_activities = ActivitiesFinder.get_activities_from_company_and_event(
        company_user.company, event
    )
    company = company_user.company

    interested_students = StudentsFinder.get_company_students(
        company_user.company, uploaded_cv=False
    )
    total_interested = len(interested_students)

    (
        total_interactions,
        total_interactions_by_activity,
        total_interactions_by_course,
        total_interactions_by_year,
        interactions_by_course,
        interactions_by_year,
    ) = get_data(
        query=get_interactions(db_session=db_session),
        event=event,
        company=company,
        group_job_fair=False,
    )

    (
        total_participations,
        total_participations_by_activity,
        total_participations_by_course,
        total_participations_by_year,
        participations_by_course,
        participations_by_year,
    ) = get_data(
        query=get_participations(company_id=company.id),
        event=event,
        company=company,
        group_job_fair=False,
    )

    return render_template(
        "companies/statistics/statistics_dashboard.html",
        participations_by_course=participations_by_course,
        participations_by_year=participations_by_year,
        interactions_by_course=interactions_by_course,
        interactions_by_year=interactions_by_year,
        total_interested=total_interested,
        total_participations_by_year=total_participations_by_year,
        total_participations=total_participations,
        total_participations_by_activity=total_participations_by_activity,
        total_participations_by_course=total_participations_by_course,
        total_interactions_by_year=total_interactions_by_year,
        total_interactions=total_interactions,
        total_interactions_by_course=total_interactions_by_course,
        total_interactions_by_activity=total_interactions_by_activity,
        activity="Total",
        company_activities=company_activities,
        error=None,
    )


@bp.post("/statistics/vue")
@requires_client_auth
def statistics_dashboard_vue():
    event = EventsFinder.get_default_event()

    print(event)

    company_name = json.loads(request.data.decode('utf-8'))['company']

    company = CompaniesFinder.get_from_name(company_name)

    print(company)
    company_activities = ActivitiesFinder.get_activities_from_company_and_event(
        company, event
    )

    interested_students = StudentsFinder.get_company_students(
        company, uploaded_cv=False
    )
    total_interested = len(interested_students)

    (
        total_interactions,
        total_interactions_by_activity,
        total_interactions_by_course,
        total_interactions_by_year,
        interactions_by_course,
        interactions_by_year,
    ) = get_data(
        query=get_interactions(db_session=db_session),
        event=event,
        company=company,
        group_job_fair=False,
    )

    (
        total_participations,
        total_participations_by_activity,
        total_participations_by_course,
        total_participations_by_year,
        participations_by_course,
        participations_by_year,
    ) = get_data(
        query=get_participations(company_id=company.id),
        event=event,
        company=company,
        group_job_fair=False,
    )

    print(total_interactions_by_activity)

    return make_response(
        jsonify({
            "participations_by_course":participations_by_course,
            "participations_by_year":participations_by_year,
            "interactions_by_course":interactions_by_course,
            "interactions_by_year":interactions_by_year,
            "total_interested":total_interested,
            "total_participations_by_year":total_participations_by_year,
            "total_participations":total_participations,
            "total_participations_by_activity":total_participations_by_activity,
            "total_participations_by_course":total_participations_by_course,
            "total_interactions_by_year":total_interactions_by_year,
            "total_interactions":total_interactions,
            "total_interactions_by_course":total_interactions_by_course,
            "total_interactions_by_activity":total_interactions_by_activity,
            "error":"",
        })
        )
