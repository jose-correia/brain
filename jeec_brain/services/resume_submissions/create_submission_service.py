import logging
from jeec_brain.models.resume_submissions import ResumeSubmissions
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class CreateSubmissionService():

    def __init__(self, kwargs: Dict):
        self.kwargs = kwargs

    def call(self) -> Optional[ResumeSubmissions]:
        
        submission = ResumeSubmissions.create(**self.kwargs)

        if not submission:
            return None

        return submission
