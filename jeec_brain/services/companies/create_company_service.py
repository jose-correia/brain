import logging
from jeec_brain.models.companies import Companies
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateCompanyService:
    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[Companies]:

        company = Companies.create(**self.kwargs)

        if not company:
            return None

        return company
