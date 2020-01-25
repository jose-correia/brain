from jeec_brain.models.resume_submissions import ResumeSubmissions


class DeleteSubmissionService():

    def __init__(self, submission: ResumeSubmissions):
        self.submission = submission

    def call(self) -> bool:
        result = self.submission.delete()
        return result
