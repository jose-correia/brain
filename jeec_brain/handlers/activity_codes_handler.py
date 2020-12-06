# SERVICES
from jeec_brain.services.activity_codes.create_activity_code_service import CreateActivityCodeService
from jeec_brain.services.activity_codes.generate_code_service import GenerateCodeService
from jeec_brain.services.activity_codes.delete_activity_code_service import DeleteActivityCodeService

# FINDERS
from jeec_brain.finders.activity_codes_finder import ActivityCodesFinder
from jeec_brain.finders.students_finder import StudentsFinder

# HANDLERS
from jeec_brain.handlers.activities_handler import ActivitiesHandler
from jeec_brain.handlers.students_handler import StudentsHandler

class ActivityCodesHandler():

    @classmethod
    def create_activity_code(cls, **kwargs):
        code = GenerateCodeService().call()

        return CreateActivityCodeService(dict(kwargs, code=code)).call()

    @classmethod
    def redeem_activity_code(cls, student, code):
        activity_code = ActivityCodesFinder.get_from_code(code)
        if(activity_code is None or activity_code.activity in student.activities):
            return None

        student_activity = StudentsFinder.get_student_activity_from_id_and_activity_id(student.id, activity_code.activity_id)
        if(student_activity is None):
            student_activity = ActivitiesHandler.add_student_activity(student, activity_code.activity)
        # else:
        #     student_activity = ActivitiesHandler.update_student_activity(student_activity, done=True)

        cls.delete_activity_code(activity_code)

        points = activity_code.activity.points
        
        return StudentsHandler.add_points(student, points)

    @classmethod
    def delete_activity_code(cls, activity_code):
        return DeleteActivityCodeService(activity_code).call()
