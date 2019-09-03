from jeec_brain.models.students import Students

class CreateStudentService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self):
        student = Students(**self.kwargs)
        
        student.create()
        student.reload()
        
        return student