from jeec_brain.models.students import Students


class StudentsFinder():

    @classmethod
    def get_from_ist_id(cls, ist_id):
        return Students.query().filter_by(ist_id=ist_id).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Students.query().filter_by(external_id=external_id).first()

    @classmethod
    def get_from_username(cls, username):
        return Students.query().filter_by(username=username).first()

    @classmethod
    def get_from_user_id(cls, user_id):
        return Students.query().filter_by(user_id=user_id).first()
    
    @classmethod
    def get_all(cls):
        return Students.all()

    @classmethod
    def get_student_activity_from_id_and_activity_id(cls, student_id, activity_id):
        return Students.query().filter_by(student_id=student_id, activity_id=activity_id).first()
    