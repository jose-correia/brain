from typing import Dict, Optional
from jeec_brain.models.companies import Companies


class UpdateCompanyService:
    def __init__(self, company: Companies, kwargs: Dict):
        self.company = company
        self.kwargs = kwargs

    def call(self) -> Optional[Companies]:
        update_result = self.company.update(**self.kwargs)
        return update_result
