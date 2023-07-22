from jeec_brain.models.levels import Levels


class LevelsFinder:
    @classmethod
    def get_level_from_external_id(cls, external_id):
        return Levels.query.filter_by(external_id=external_id).first()

    @classmethod
    def get_all_levels(cls):
        return Levels.query.order_by(Levels.value).all()

    @classmethod
    def get_level_by_value(cls, value):
        return Levels.query.filter_by(value=value).first()

    @classmethod
    def get_levels_from_parameters(cls, kwargs):
        try:
            return Levels.query.filter_by(**kwargs).all()
        except Exception:
            return None
