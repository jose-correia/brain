import logging
from jeec_brain.models.companies import Companies
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateCompanyService():

    def __init__(self, payload: Dict):
        self.name = payload.get('name')
        self.email = payload.get('email')
        self.link = payload.get('link')
        self.access_cv_platform = payload.get('access_cv_platform')
        self.business_area = payload.get('business_area')
        self.partnership_tier = payload.get('partnership_tier')

    def call(self) -> Optional[Companies]:
        
        company = Companies.create(
            name=self.name,
            email=self.email,
            link=self.link,
            partnership_tier=self.partnership_tier,
            access_cv_platform=self.access_cv_platform,
            business_area=self.business_area
        )

        if not company:
            return None

        return company
