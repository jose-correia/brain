from jeec_brain.models.student_referrals import StudentReferrals


class DeleteStudentReferralService():

    def __init__(self, student_referral: StudentReferrals):
        self.student_referral = student_referral

    def call(self) -> bool:
        result = self.student_referral.delete()
        return result
