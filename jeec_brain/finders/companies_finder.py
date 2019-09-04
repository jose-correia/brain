from jeec_brain.models.companies import Companies


class CompaniesFinder():

    @classmethod
    def get_from_username(cls, username):
        return Companies.query.filter_by(username=username).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Companies.query.filter_by(external_id=external_id).first()
    
    @classmethod
    def get_from_email(cls, email):
        return Companies.query.filter_by(email=email).first()
    
    @classmethod
    def get_all(cls):
        return Companies.query.order_by(Companies.name)
    
    @classmethod
    def get_all_with_cv_access(cls):
        return Companies.query.filter_by(access_cv_platform=True)

    @classmethod
    def get_from_external_id(cls, external_id):
        return Companies.query.filter_by(external_id=external_id).first()
        