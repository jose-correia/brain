from jeec_brain.values.value_composite import ValueComposite


class SquadInvitationsSentValue(ValueComposite):
    def __init__(self, students):
        super(SquadInvitationsSentValue, self).initialize({})
        students_array = []
        for student in students:
            student_value = {
                "name": student.user.name,
                "ist_id": student.user.username,
                "level": student.level.value,
                "photo": "data: " + student.photo_type + ";base64, " + student.photo,
                "id": student.id,
            }
            students_array.append(student_value)
        self.serialize_with(data=students_array)
