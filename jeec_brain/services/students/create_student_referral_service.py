import logging
from jeec_brain.models.student_referrals import StudentReferrals
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateStudentReferralService:
    def __init__(self, **kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[StudentReferrals]:

        student_referral = StudentReferrals.create(**self.kwargs)

        if not student_referral:
            return None

        return student_referral
