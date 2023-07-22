from jeec_brain.models.companies import Companies


class DeleteCompanyService:
    def __init__(self, company: Companies):
        self.company = company

    def call(self) -> bool:
        result = self.company.delete()
        return result
