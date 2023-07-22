# SERVICES
from jeec_brain.services.tags.create_tag_service import CreateTagService
from jeec_brain.services.tags.delete_tag_service import DeleteTagService
from jeec_brain.services.tags.update_tag_service import UpdateTagService
from jeec_brain.services.tags.add_student_tag_service import AddStudentTagService
from jeec_brain.services.tags.delete_student_tag_service import DeleteStudentTagService
from jeec_brain.services.tags.update_student_tag_service import UpdateStudentTagService
from jeec_brain.services.tags.add_activity_tag_service import AddActivityTagService
from jeec_brain.services.tags.update_activity_tag_service import (
    UpdateActivityTagService,
)
from jeec_brain.services.tags.delete_activity_tag_service import (
    DeleteActivityTagService,
)


class TagsHandler:
    @classmethod
    def create_tag(cls, **kwargs):
        return CreateTagService(kwargs=kwargs).call()

    @classmethod
    def update_tag(cls, tag, **kwargs):
        return UpdateTagService(tag=tag, kwargs=kwargs).call()

    @classmethod
    def delete_tag(cls, tag):
        return DeleteTagService(tag=tag).call()

    @classmethod
    def add_student_tag(cls, student, tag):
        return AddStudentTagService(student.id, tag.id).call()

    @classmethod
    def update_student_tag(cls, student_tag, **kwargs):
        return UpdateStudentTagService(student_tag, kwargs).call()

    @classmethod
    def delete_student_tag_service(cls, student_tag):
        return DeleteStudentTagService(student_tag).call()

    @classmethod
    def add_activity_tag(cls, activity, tag):
        return AddActivityTagService(activity.id, tag.id).call()

    @classmethod
    def update_activity_tag(cls, activity_tag, **kwargs):
        return UpdateActivityTagService(activity_tag, kwargs).call()

    @classmethod
    def delete_activity_tag(cls, activity_tag):
        return DeleteActivityTagService(activity_tag).call()
