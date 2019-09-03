from jeec_brain.models.companies import Companies

class CreateCompanyService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self):
        try:
            company = Companies(**self.kwargs)

            company.create()
            company.reload()
            
        except Exception:
            return None

        return company