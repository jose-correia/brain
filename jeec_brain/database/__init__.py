import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()
db.UUID = UUID(as_uuid=True)
db_session = db.session


def create_tables():
    # Event
    from jeec_brain.models.events import Events
    
    from jeec_brain.models.colaborators import Colaborators
    from jeec_brain.models.speakers import Speakers
    from jeec_brain.models.users import Users
    from jeec_brain.models.teams import Teams

    # Activities
    from jeec_brain.models.activity_types import ActivityTypes
    from jeec_brain.models.activities import Activities
    from jeec_brain.models.company_activities import CompanyActivities
    from jeec_brain.models.speaker_activities import SpeakerActivities
    from jeec_brain.models.activities_tags import ActivitiesTags
    from jeec_brain.models.activity_codes import ActivityCodes

    # Companies
    from jeec_brain.models.company_users import CompanyUsers
    from jeec_brain.models.companies import Companies
    from jeec_brain.models.companies_tags import CompaniesTags

    # Auctions
    from jeec_brain.models.auctions import Auctions
    from jeec_brain.models.company_auctions import CompanyAuctions
    from jeec_brain.models.bids import Bids

    # Resumes
    from jeec_brain.models.resume_submissions import ResumeSubmissions
    from jeec_brain.models.company_resume_submissions import CompanyResumeSubmissions

    # Meals
    from jeec_brain.models.meals import Meals
    from jeec_brain.models.dishes import Dishes
    from jeec_brain.models.company_meals import CompanyMeals
    from jeec_brain.models.company_dishes import CompanyDishes

    # Students
    from jeec_brain.models.students import Students
    from jeec_brain.models.levels import Levels
    from jeec_brain.models.squads import Squads
    from jeec_brain.models.squad_invitations import SquadInvitations
    from jeec_brain.models.student_activities import StudentActivities
    from jeec_brain.models.student_companies import StudentCompanies
    from jeec_brain.models.students_tags import StudentsTags
    from jeec_brain.models.tags import Tags
    from jeec_brain.models.banned_students import BannedStudents
    from jeec_brain.models.student_logins import StudentLogins

    # Rewards
    from jeec_brain.models.rewards import Rewards
    from jeec_brain.models.jeecpot_rewards import JeecpotRewards
    from jeec_brain.models.squads_rewards import SquadsRewards

    db.create_all()


def drop_tables():
    db.reflect()
    db.drop_all()


def create_testing_db():
    conn = db.engine.connect()
    conn.execute('commit')  # stop open transaction
    conn.execute('create database test_' + os.environ['APP_DB'])
    conn.close()