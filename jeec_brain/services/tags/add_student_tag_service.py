from typing import Optional
from jeec_brain.models.students_tags import StudentsTags


class AddStudentTagService(object):
    def __init__(self, student_id, tag_id):
        self.student_id = student_id
        self.tag_id = tag_id

    def call(self) -> Optional[StudentsTags]:
        student_tag = StudentsTags.create(
            student_id=self.student_id, tag_id=self.tag_id
        )
        return student_tag
