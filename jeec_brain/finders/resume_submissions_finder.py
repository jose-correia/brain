from jeec_brain.database import db_session
from jeec_brain.models.resume_submissions import ResumeSubmissions
from sqlalchemy import text


class ResumeSubmissionsFinder():

    @classmethod
    def get_all(cls):
        return ResumeSubmissions.query().order_by(ResumeSubmissions.name).all()

    @classmethod
    def get_submission_by_external_id(cls, external_id):
        return ResumeSubmissions.query().filter_by(external_id=external_id).first()

    @classmethod
    def get_submission_by_name(cls, name):
        return ResumeSubmissions.query().filter_by(name=name).first()

    @classmethod
    def get_not_participants(cls, submission):
        command = text (
            """
                SELECT
                    *
                FROM
                    companies as c
                WHERE
                    c.id 
                NOT IN (
                    SELECT
                        c2.id
                    FROM
                        companies as c2
                    INNER JOIN
                        company_resume_submissions as c_sub2
                    ON
                        c2.id = c_sub2.company_id
                    AND
                        c_sub2.resume_submission_id=:submission_id
                );"""
        )
        return db_session.execute(command, {"submission_id": submission.id,}).fetchall()
