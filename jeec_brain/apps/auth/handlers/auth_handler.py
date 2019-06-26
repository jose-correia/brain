from flask import session
from jeec_brain.apps.auth.services.create_student_service import CreateStudentService
from jeec_brain.apps.auth.finders.student_finder import StudentFinder

import logging
logger = logging.getLogger(__name__)

class AuthHandler(object):

    @staticmethod
    def check_for_user():
        student = StudentFinder.get_from_istid(session['username'])

        if student is None:
            logger.info("New user acessing the platform.")
            try:
                CreateStudentService(istid=session['username'], name=session['name']).call()
                logger.info("New student added to the DB")
                session['first_time_login'] = True
                return False
            except Exception as e:
                logger.error(e)
        else:
            if student.acceptedTerms == False: #if the user never authenticated show terms
                session['first_time_login'] = True
            else:
                session['first_time_login'] = False
            return True

    # @staticmethod
    # def check_for_company():
    #     company = CompanyFinder.get_from_username(session['company_username'])

    #     if company is None:
    #         logger.info("New company added to the platform.")
    #         try:
    #             CreateCompanyService()