from jeec_brain.database import db
from jeec_brain.models.model_mixin import ModelMixin


class News(ModelMixin, db.Model):
    __tablename__ = 'news'
    
    description = db.Column(db.String(300))
    day = db.Column(db.String(20))
    video_url = db.Column(db.String(100))

    def __repr__(self):
        return 'Day: {}'.format(self.day)
