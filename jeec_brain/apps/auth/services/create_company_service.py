from jeec_brain.models.company import Company

class CreateUserService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self):
        company = Company(**self.kwargs)

        company.create()
        company.reload()
        
        return company