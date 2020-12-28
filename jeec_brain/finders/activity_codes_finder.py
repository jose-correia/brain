from jeec_brain.models.activity_codes import ActivityCodes


class ActivityCodesFinder():

    @classmethod
    def get_from_code(cls, code):
        return ActivityCodes.query.filter_by(code=code).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return ActivityCodes.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_all(cls):
        return ActivityCodes.all()

    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            return ActivityCodes.query.filter_by(**kwargs).all()
        except Exception:
            return None
