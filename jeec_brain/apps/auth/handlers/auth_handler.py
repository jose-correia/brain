from flask import session, redirect
import os
import jwt
from config import Config
from flask_login import login_user, logout_user, current_user
from jeec_brain.apps.auth import fenix_client
from jeec_brain.finders.events_finder import EventsFinder

# handlers
from jeec_brain.apps.auth.handlers.tecnico_client_handler import TecnicoClientHandler
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.students_handler import StudentsHandler
from jeec_brain.handlers.schedule_student_handler import ScheduleStudentHandler


# services
from jeec_brain.apps.auth.services.encrypt_token_service import EncryptTokenService
from jeec_brain.services.users.generate_credentials_service import (
    GenerateCredentialsService,
)

# finders
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.users_finder import UsersFinder
from jeec_brain.finders.schedule_student_finder import ScheduleStudentFinder


from jeec_brain.models.enums.roles_enum import RolesEnum

import logging
import fenixedu
import datetime


logger = logging.getLogger(__name__)


class AuthHandler(object):
    @staticmethod
    def redirect_to_fenix_login():
        url = TecnicoClientHandler.get_authentication_url(fenix_client)
        return redirect(url, code=302)


    @staticmethod
    def get_student_classes(person_schedule):
        #print(person_schedule)
        
        event = EventsFinder.get_default_event()
        jeec_start = event.start_date
        jeec_end = event.end_date
        jeec_start_day = int(jeec_start[0:2])
        jeec_end_day = int(jeec_end[0:2])
        jeec_start_month = int(jeec_start[3:6])
        jeec_end_month = int(jeec_end[3:6])
        jeec_start_year = int(jeec_start[6:10])
        jeec_end_year = int(jeec_end[6:10])
        print(jeec_start)
        print(jeec_end)
        #print(jeec_end_day)
        #print(jeec_end_month)
        #print(jeec_end_year)
        # print(jeec_start) 08 Mar 2023, Wed
        
        jeec_start_total = jeec_start_day + 31 * jeec_start_month + 365 * jeec_start_year
        jeec_end_total = jeec_end_day + 31 * jeec_end_month + 365 * jeec_end_year
        
        classes = []
        i=0
        
        for classs in person_schedule['events']:
            class_start = classs['classPeriod']['start']
            class_end = classs['classPeriod']['end']
            # classperiod.start 18/09/2013 17:30 
            class_start_day = int(class_start[0:2])
            class_end_day = int(class_end[0:2])
            class_start_month = int(class_start[3:5])
            class_end_month = int(class_end[3:5])
            class_start_year = int(class_start[6:10])
            class_end_year = int(class_end[6:10])
            if class_start_year == 2023:

            
                #print('start')
                #print(class_start_day)
                #print(class_start_month)
                #print(class_start_year)
                
                #print('end')
                #print(class_end_day)
                #print(class_end_month)
                #print(class_end_year)
                
                class_start_total = class_start_day + 31 * class_start_month + 365 * class_start_year
                class_end_total = class_end_day + 31 * class_end_month + 365 * class_end_year
                
                #print(class_start_total)
                #print(jeec_start_total)
                #print(class_end_total)
                #print(jeec_end_total)
                #print()
                    
                if (class_start_total >= jeec_start_total and class_end_total <= jeec_end_total):
                    #print('Entrei')
                    i = i + 1
                    new_class = {
                        'id': i + 1,
                        'start': class_start[6] + class_start[7] + class_start[8] + class_start[9] + '-' + class_start[3] + class_start[4] + 
                        '-' + class_start[0] + class_start[1] + 'T' + class_start[11] + class_start[12] + ':' + class_start[14] + class_start[15] + ':00',
                        'end': class_end[6] + class_end[7] + class_end[8] + class_end[9] + '-' + class_end[3] + class_end[4] + 
                        '-' + class_end[0] + class_end[1] + 'T' + class_end[11] + class_end[12] + ':' + class_end[14] + class_end[15] + ':00',
                        'text': classs['course']['acronym'] + '  ' + classs['location'][0]['name'],
                        'backColor': "#585c61",
                        'borderColor': "#585c61",  
                        'type': "event",
                    }
                    #print(new_class)
                    classes.append(new_class)
                    #print(classes)
        return classes
        
    
    @staticmethod
    def login_student(fenix_auth_code):
        if fenix_auth_code is not None:
            user = TecnicoClientHandler.get_user(fenix_client, fenix_auth_code)
            person = TecnicoClientHandler.get_person(fenix_client, user)
            
            person_schedule = TecnicoClientHandler.get_person_classes_calendar(fenix_client, user)

            classes = AuthHandler.get_student_classes(person_schedule)
            print(classes)
            
            student_scheduleee = ScheduleStudentFinder.get_from_student_id(person['username'])
            #ScheduleStudentHandler.delete_schedule_student(student_scheduleee)
            
            if student_scheduleee == None:
                ScheduleStudentHandler.create_schedule_student(student_id=person['username'], classes=str(classes), activities = str([]), showFenix=True) 
            else:
                ScheduleStudentHandler.update_schedule_student(student_scheduleee, student_id=person['username'], classes=str(classes), activities = student_scheduleee.activities,showFenix=student_scheduleee.showFenix) 
            
            banned_ids = StudentsFinder.get_banned_students_ist_id()
            if person["username"] in banned_ids:
                return None, None

            student = StudentsFinder.get_from_ist_id(person["username"])
            if student is None:
                course = None
                for role in person["roles"]:
                    if role["type"] == "STUDENT":
                        for registration in role["registrations"]:
                            if registration["acronym"]:
                                course = registration["acronym"]
                                entry_year = get_year(registration["academicTerms"])
                                break
                    if role["type"] == "ALUMNI":
                        for registration in role["concludedRegistrations"]:
                            if registration["acronym"]:
                                course = registration["acronym"]
                                entry_year = get_year(registration["academicTerms"])
                                break

                if not course:
                    return None, None

                if person["email"]:
                    email = person["email"]
                elif person["institutionalEmail"]:
                    email = person["institutionalEmail"]
                else:
                    return None, None

                student = StudentsHandler.create_student(
                    Config.ROCKET_CHAT_ENABLE,
                    person["name"],
                    person["username"],
                    email,
                    course,
                    entry_year,
                    person["photo"]["data"],
                    person["photo"]["type"],
                )
                if student is None:
                    return None, None

            _jwt = jwt.encode(
                {"user_id": person["username"]}, Config.JWT_SECRET, algorithm="HS256"
            )
            encrypted_jwt = EncryptTokenService(_jwt).call()

            return student, encrypted_jwt

        else:
            return None, None
        
    

    @staticmethod
    def login_company(username, password):
        user = UsersFinder.get_user_from_credentials(username, password)

        if user is None:
            logger.warning(
                f"User tried to authenticate with credentials: {username}:{password}"
            )
            return False

        company_user = UsersFinder.get_company_user_from_user(user)
        if company_user is None:
            logger.warning(
                f"User tried to authenticate with credentials: {username}:{password}"
            )
            return False

        if user.role.name != "company" or company_user.company is None:
            logger.warning(
                f"""User without company role, tried to login as company! username: {username}"""
            )
            return False

        login_user(user)
        return True, None

    @staticmethod
    def login_admin_dashboard(username, password):
        user = UsersFinder.get_user_from_credentials(username, password)

        if user is None:
            logger.warning(
                f"User tried to authenticate with credentials: {username}:{password}"
            )
            return False

        if user.role.name in [
            "admin",
            "companies_admin",
            "speakers_admin",
            "teams_admin",
            "activities_admin",
            "viewer",
        ]:
            login_user(user)
            return True
        return False

    @staticmethod
    def logout_user():
        logout_user()


def get_year(academicTerms):
    if len(academicTerms) == 0:
        return ""

    terms = [academicTerm[11:].replace(" ", "") for academicTerm in academicTerms]
    terms.sort()
    return terms[0]
