from typing import Optional
from jeec_brain.models.company_resume_submissions import CompanyResumeSubmissions


class AddSubmissionParticipantService():
    def __init__(self, company_id: int, submission_id: int):
        self.company_id = company_id
        self.submission_id = submission_id

    def call(self) -> Optional[CompanyResumeSubmissions]:
        company_resume_submission = CompanyResumeSubmissions.create(
            company_id=self.company_id,
            resume_submission_id=self.submission_id
        )
        return company_resume_submission
