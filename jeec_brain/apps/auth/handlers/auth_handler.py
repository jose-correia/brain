from flask import session, redirect
import os
from flask_login import login_user, logout_user, current_user
from jeec_brain.apps.auth import fenix_client

# handlers
from jeec_brain.apps.auth.handlers.tecnico_client_handler import TecnicoClientHandler

# services
from jeec_brain.services.students.create_student_service import CreateStudentService
from jeec_brain.services.users.create_user_service import CreateUserService

# finders
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.users_finder import UsersFinder

from jeec_brain.models.enums.roles_enum import RolesEnum

import logging
logger = logging.getLogger(__name__)

class AuthHandler(object):
    @staticmethod
    def redirect_to_fenix_login():
        url = TecnicoClientHandler.get_authentication_url(fenix_client)
        return redirect(url, code=302)

    
    @staticmethod
    def login_student(fenix_auth_code):
        if fenix_auth_code is not None:            
            user = TecnicoClientHandler.get_user(fenix_client, fenix_auth_code)
            person = TecnicoClientHandler.get_person(fenix_client, user)
        
            session['name'] = person['name']
            session['username'] = person['username']

            user = UserFinder.get_user_from_username(person['username'])

            if user is None:
                try:
                    user = CreateUserService(username=person['username'], role="student").call()
                    logger.info("New user added to the DB")    

                    student = CreateStudentService(ist_id=person['username'], name=person['name']).call()
                    student.user_id = user.uuid
                except Exception as e:
                    logger.error(e)
                    return False, e

            student = StudentsFinder.get_from_ist_id(ist_id=person['username'])

            if student is None:
                try:
                    student = CreateStudentService(ist_id=person['username'], name=person['name']).call()
                    student.user_id = user.uuid
                except Exception as e:
                    logger.error(e)
                    return False, e
            
            session['STUDENT'] = student.name
            login_user(user)
            logger.info("Student authenticated! ist_id: {}".format(user.username))
            return True, None
                    
        else:
            return False, "Failed to fetch Fenix_Auth_Code"

    
    @staticmethod
    def login_company(username, password):
        user = UsersFinder.get_user_from_credentials(username, password)

        if user is None:
            logger.warning(f"User tried to authenticate with credentials: {username}:{password}")
            return False

        if user.role.name != 'company' or user.company is None:
            logger.warning(f'''User without company role, tried to login as company! username: {username}''')
            return False

        login_user(user)
        return True, None
        

    @staticmethod
    def login_admin_dashboard(username, password):
        user = UsersFinder.get_user_from_credentials(username, password)

        if user is None:
            logger.warning(f"User tried to authenticate with credentials: {username}:{password}")
            return False

        if user.role.name in ['admin', 'companies_admin', 'speakers_admin', 'teams_admin', 'activities_admin', 'viewer']:
            login_user(user)
            return True
        return False


    @staticmethod
    def logout_user():
        logout_user()
