from typing import Dict, Optional
from jeec_brain.models.students_tags import StudentsTags


class UpdateStudentTagService():
    
    def __init__(self, student_tag: StudentsTags, kwargs: Dict):
        self.student_tag = student_tag
        self.kwargs = kwargs

    def call(self) -> Optional[StudentsTags]:
        update_result = self.student_tag.update(**self.kwargs)
        return update_result
