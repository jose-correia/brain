from jeec_brain.models.banned_students import BannedStudents

class CreateBannedStudentService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self):        
        banned_student = BannedStudents.create(**self.kwargs)

        if not banned_student:
            return None

        return banned_student