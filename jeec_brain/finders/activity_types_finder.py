from jeec_brain.models.activity_types import ActivityTypes


class ActivityTypesFinder:
    @classmethod
    def get_from_name(cls, name):
        return ActivityTypes.query.filter_by(name=name).first()

    @classmethod
    def get_from_external_id(cls, external_id):
        return ActivityTypes.query.filter_by(external_id=external_id).first()

    @classmethod
    def get_all_from_event(cls, event):
        return ActivityTypes.query.filter_by(event=event).all()

    @classmethod
    def get_all(cls):
        return ActivityTypes.query.order_by(ActivityTypes.updated_at).all()

    @classmethod
    def get_from_parameters(cls, kwargs):
        try:
            return ActivityTypes.query.filter_by(**kwargs).all()
        except Exception:
            return None
