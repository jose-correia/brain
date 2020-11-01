from jeec_brain.models.students import Students

class CreateStudentService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self):        
        student = Students.create(**self.kwargs)

        if not student:
            return None

        return student