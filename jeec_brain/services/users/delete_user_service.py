from jeec_brain.models.users import Users
from jeec_brain.database import db


class DeleteUserService:
    def __init__(self, user: Users):
        self.user = user

    def call(self) -> bool:

        try:
            db.session.delete(self.user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False

        return True
