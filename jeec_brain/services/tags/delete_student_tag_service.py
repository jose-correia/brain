from jeec_brain.models.students_tags import StudentsTags


class DeleteStudentTagService():

    def __init__(self, student_tag: StudentsTags):
        self.student_tag = student_tag

    def call(self) -> bool:
        result = self.student_tag.delete()
        return result
