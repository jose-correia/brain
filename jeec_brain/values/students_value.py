import jwt
from config import Config
from jeec_brain.values.value_composite import ValueComposite
from jeec_brain.values.levels_value import LevelsValue
from jeec_brain.values.squads_value import SquadsValue


class StudentsValue(ValueComposite):
    def __init__(self, students, details):
        super(StudentsValue, self).initialize({})

        if not isinstance(students, list):
            students = [students]

        students_array = []
        for student in students:

            student_value = {
                "name": student.user.name,
                "photo": "data: " + student.photo_type + ";base64, " + student.photo,
                "ist_id": student.user.username,
                "level": LevelsValue(student.level).to_dict()
                if student.level
                else LevelsValue(None).to_dict(),
                "total_points": student.total_points,
            }
            if details:
                student_details = {
                    # "jwt": jwt.encode({"user_id": student.user.username}, Config.JWT_SECRET, algorithm="HS256"),
                    "email": student.user.email,
                    "daily_points": student.daily_points,
                    "squad_points": student.squad_points,
                    "linkedin_url": student.linkedin_url,
                    "uploaded_cv": student.uploaded_cv,
                    "companies": [company.name for company in student.companies],
                    "tags": [tag.name for tag in student.tags],
                    "login_dates": [
                        login_date.date for login_date in student.login_dates
                    ],
                    "referral_code": student.referral_code,
                }

                students_array.append({**student_value, **student_details})
            else:
                students_array.append(student_value)

        if len(students_array) == 1:
            self.serialize_with(data=students_array[0])
        else:
            self.serialize_with(data=students_array)
