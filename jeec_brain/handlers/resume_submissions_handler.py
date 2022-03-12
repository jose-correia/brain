# SERVICES
from jeec_brain.services.resume_submissions.create_submission_service import (
    CreateSubmissionService,
)
from jeec_brain.services.resume_submissions.update_submission_service import (
    UpdateSubmissionService,
)
from jeec_brain.services.resume_submissions.delete_submission_service import (
    DeleteSubmissionService,
)
from jeec_brain.services.resume_submissions.add_submission_participant_service import (
    AddSubmissionParticipantService,
)


class ResumeSubmissionsHandler:
    @classmethod
    def create_submission(cls, **kwargs):
        return CreateSubmissionService(kwargs=kwargs).call()

    @classmethod
    def update_submission(cls, submission, **kwargs):
        return UpdateSubmissionService(submission=submission, kwargs=kwargs).call()

    @classmethod
    def delete_submission(cls, submission):
        return DeleteSubmissionService(submission=submission).call()

    @classmethod
    def add_submission_participant(cls, submission, company):
        return AddSubmissionParticipantService(
            submission_id=submission.id, company_id=company.id
        ).call()
