from jeec_brain.models.student import Student

class CreateStudentService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self):
        student = Student(**self.kwargs)
        
        student.create()
        student.reload()
        
        return student