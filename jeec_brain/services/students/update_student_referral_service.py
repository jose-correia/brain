from typing import Dict, Optional
from jeec_brain.models.student_referrals import StudentReferrals


class UpdateStudentReferralService:
    def __init__(self, student_referral: StudentReferrals, kwargs: Dict):
        self.student_referral = student_referral
        self.kwargs = kwargs

    def call(self) -> Optional[StudentReferrals]:
        update_result = self.student_referral.update(**self.kwargs)
        return update_result
