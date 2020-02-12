from typing import Dict, Optional
from jeec_brain.models.resume_submissions import ResumeSubmissions


class UpdateSubmissionService():
    
    def __init__(self, submission: ResumeSubmissions, kwargs: Dict):
        self.submission = submission
        self.kwargs = kwargs

    def call(self) -> Optional[ResumeSubmissions]:
        update_result = self.submission.update(**self.kwargs)
        return update_result
