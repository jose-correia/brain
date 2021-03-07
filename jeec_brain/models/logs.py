from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin
from sqlalchemy.orm import relationship


class Logs(db.Model, ModelMixin):
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.String(20))
    entrypoint = db.Column(db.String(200), nullable=False)
    create_date = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return 'Id: {}'.format(self.id)
