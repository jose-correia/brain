from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import TIMESTAMP

from jeec_brain.database import db_session

from sqlalchemy_utils import UUIDType
import uuid
from flask import current_app

from datetime import datetime


class ModelMixin():
    __mapper_args__ = {'always_refresh': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
    external_id = Column(UUIDType(binary=False), default=uuid.uuid4, index=True)

    _repr_hide = ['created_at', 'updated_at']

    @classmethod
    def query(cls):
        try:
            result = db_session.query(cls)
            db_session.commit()
            return result
        except Exception as e:
            current_app.logger.info(e)
            db_session.rollback()
            return None

    @classmethod
    def all(cls):
        try:
            result = db_session.query(cls).all()
            db_session.commit()
            return result
        except Exception as e:
            current_app.logger.info(e)
            db_session.rollback()
            return None

    @classmethod
    def delete_all(cls):
        try:
            db_session.query(cls).delete()
            db_session.commit()
        except Exception as e:
            current_app.logger.info(e)
            db_session.rollback()
        return

    @classmethod
    def first(cls):
        try:
            result = db_session.query(cls).first()
            db_session.commit()
            return result
        except Exception as e:
            current_app.logger.info(e)
            db_session.rollback()
            return None

    @classmethod
    def last(cls):
        try:
            result = db_session.query(cls).order_by(cls.created_at.desc()).first()
            db_session.commit()
            return result
        except Exception as e:
            current_app.logger.info(e)
            db_session.rollback()
            return None

    @classmethod
    def get(cls, id):
        try:
            result = cls.query.get(id)
            db_session.commit()
            return result
        except Exception as e:
            current_app.logger.info(e)
            db_session.rollback()
            return None

    @classmethod
    def get_by(cls, **kw):
        try:
            result = cls.query.filter_by(**kw).first()
            db_session.commit()
            return result
        except Exception as e:
            current_app.logger.info(e)
            db_session.rollback()
            return None

    @classmethod
    def get_or_create(cls, **kw):
        r = cls.get_by(**kw)
        if not r:
            r = cls(**kw)
            try:
                db_session.add(r)
                db_session.commit()
            except Exception as e:
                current_app.logger.info(e)
                db_session.rollback()
        return r

    @classmethod
    def create(cls, **kw):
        r = cls(**kw)
        try:
            db_session.add(r)
            db_session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db_session.rollback()
            return None
        else:
            return r

    def save(self):
        try:
            db_session.add(self)
            db_session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db_session.rollback()
        return self

    def delete(self) -> bool:
        try:
            db_session.delete(self)
            db_session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db_session.rollback()
            return False
        else:
            return True

    def update(self, **kwargs):
        '''
            Updates the model's fields and returns the model instance if sucessful
        '''
        try:
            db_session.query(self.__class__).filter_by(id=self.id).update(
                kwargs)
            db_session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db_session.rollback()
            return None
        else:
            return self

    def __repr__(self):
        values = ', '.join(
            "%s=%r" % (n, getattr(self, n)) for n in self.__table__.c.keys() if
            n not in self._repr_hide)
        return "%s(%s)" % (self.__class__.__name__, values)

    def filter_string(self):
        return self.__str__()
