import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()
db.UUID = UUID(as_uuid=True)
db_session = db.session


def create_tables():
    from jeec_brain.models.companies import Companies
    from jeec_brain.models.students import Students
    from jeec_brain.models.activities import Activities
    from jeec_brain.models.colaborators import Colaborators
    from jeec_brain.models.speakers import Speakers
    from jeec_brain.models.users import Users
    from jeec_brain.models.teams import Teams
    from jeec_brain.models.event_information import EventInformation
    db.create_all()


def drop_tables():
    db.reflect()
    db.drop_all()


def create_testing_db():
    conn = db.engine.connect()
    conn.execute('commit')  # stop open transaction
    conn.execute('create database test_' + os.environ['APP_DB'])
    conn.close()