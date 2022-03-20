from jeec_brain.models.students import Students
from jeec_brain.models.banned_students import BannedStudents
from jeec_brain.models.users import Users
from jeec_brain.models.levels import Levels
from jeec_brain.models.squads import Squads
from jeec_brain.models.student_activities import StudentActivities
from jeec_brain.models.student_companies import StudentCompanies
from jeec_brain.models.student_logins import StudentLogins
from jeec_brain.models.student_referrals import StudentReferrals


class StudentsFinder:
    @classmethod
    def get_from_ist_id(cls, ist_id):
        return Students.query.filter(
            (Students.user_id == Users.id) & (Users.username == ist_id)
        ).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return Students.query.filter_by(external_id=external_id).first()

    @classmethod
    def get_from_id(cls, id):
        return Students.query.filter_by(id=id).first()

    @classmethod
    def get_from_username(cls, username):
        return Students.query.filter_by(username=username).first()

    @classmethod
    def get_from_user_id(cls, user_id):
        return Students.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_from_referral_code(cls, code):
        return Students.query.filter_by(referral_code=code).first()

    @classmethod
    def get_from_level_or_higher(cls, level):
        return Students.query.filter(
            Students.level_id == Levels.id, Levels.value >= level.value
        ).all()

    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            students = Students.query.filter_by(**kwargs).all()
        except Exception:
            return None

        return students

    @classmethod
    def get_all(cls):
        return Students.all()

    @classmethod
    def get_all_simple(cls):
        return (
            Students.query.join(Users, Students.user_id == Users.id)
            .join(Levels, Students.level_id == Levels.id, isouter=True)
            .join(Squads, Students.squad_id == Squads.id, isouter=True)
            .with_entities(
                Users.name,
                Users.username,
                Users.email,
                Students.linkedin_url,
                Levels.value,
                Students.daily_points,
                Students.total_points,
                Students.uploaded_cv,
                Squads.name,
                Students.external_id,
                Students.id,
            )
            .all()
        )

    @classmethod
    def get_top(cls, number=10):
        return Students.query.order_by(Students.total_points.desc()).limit(number).all()

    @classmethod
    def get_from_search(cls, search):
        search = "%{}%".format(search)
        return (
            Students.query.join(Users, Students.user_id == Users.id)
            .join(Levels, Students.level_id == Levels.id, isouter=True)
            .join(Squads, Students.squad_id == Squads.id, isouter=True)
            .filter(
                (Students.user_id == Users.id)
                & (Users.name.ilike(search) | Users.username.ilike(search))
            )
            .with_entities(
                Users.name,
                Users.username,
                Users.email,
                Students.linkedin_url,
                Levels.value,
                Students.daily_points,
                Students.total_points,
                Students.uploaded_cv,
                Squads.name,
                Students.external_id,
                Students.id,
            )
            .all()
        )

    @classmethod
    def get_from_search_without_student(cls, search, student_external_id):
        search = "%{}%".format(search)
        return Students.query.filter(
            (Students.user_id == Users.id)
            & (Users.name.ilike(search) | Users.username.ilike(search))
            & (Students.external_id != student_external_id)
        ).all()

    @classmethod
    def get_student_activity_from_id_and_activity_id(cls, student_id, activity_id):
        return StudentActivities.query.filter_by(
            student_id=student_id, activity_id=activity_id
        ).first()

    @classmethod
    def get_student_activities_from_student_id(cls, student_id):
        return StudentActivities.query.filter_by(student_id=student_id).all()

    @classmethod
    def get_students_from_activity_id(cls, activity_id):
        return (
            Students.query.join(
                StudentActivities, (StudentActivities.student_id == Students.id)
            )
            .filter(StudentActivities.activity_id == activity_id)
            .order_by(Students.id)
            .all()
        )

    @classmethod
    def get_student_company(cls, student, company):
        return StudentCompanies.query.filter_by(
            student_id=student.id, company_id=company.id
        ).first()

    @classmethod
    def get_student_login(cls, student, date):
        return StudentLogins.query.filter_by(student_id=student.id, date=date).first()

    @classmethod
    def get_banned_students_ist_id(cls):
        return [
            r[0]
            for r in BannedStudents.query.with_entities(BannedStudents.ist_id).all()
        ]

    @classmethod
    def get_banned_student_from_external_id(cls, external_id):
        return BannedStudents.query.filter_by(external_id=external_id).first()

    @classmethod
    def get_all_banned(cls):
        return BannedStudents.all()

    @classmethod
    def get_referral_redeemer(cls, redeemer):
        return StudentReferrals.query.filter_by(redeemer_id=redeemer.id).first()

    @classmethod
    def get_cv_students(cls):
        return Students.query.filter_by(uploaded_cv=True).all()

    @classmethod
    def get_company_students(cls, company, uploaded_cv: bool):
        return (
            Students.query.join(
                StudentCompanies,
                (StudentCompanies.student_id == Students.id)
                & (StudentCompanies.company_id == company.id),
            )
            .join(Users, Students.user_id == Users.id)
            .with_entities(
                Students.entry_year,
                Students.course,
                Students.linkedin_url,
                Students.external_id,
                Users.name,
                Users.email,
                StudentCompanies.company_id,
            )
            .filter((Students.uploaded_cv == uploaded_cv) if uploaded_cv else True)
            .all()
        )
