import sqlalchemy
from jeec_brain.models.student import Student

class StudentFinder(object):

    @classmethod
    def get_from_istid(cls, istid):
        return Student.query.filter_by(istid=istid).first()