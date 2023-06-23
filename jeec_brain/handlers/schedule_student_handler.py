# SERVICES
from flask import current_app
from jeec_brain.services.schedule.create_student_schedule import CreateScheduleStudentService
from jeec_brain.services.schedule.update_student_schedule import UpdateScheduleStudentService
from jeec_brain.services.schedule.delete_student_schedule import DeleteScheduleStudentService


class ScheduleStudentHandler:
    @classmethod
    def create_schedule_student(cls, **kwargs):
        return CreateScheduleStudentService(kwargs=kwargs).call()

    @classmethod
    def update_schedule_student(cls, schedule_student, **kwargs):
        return UpdateScheduleStudentService(schedule_student=schedule_student, kwargs=kwargs).call()
    
    @classmethod
    def delete_schedule_student(cls, schedule_student):
        return DeleteScheduleStudentService(schedule_student=schedule_student).call()