from jeec_brain.models.reward_student import StudentRewards

class StudentRewardsFinder:
    @classmethod
    def get_all(cls):
        return StudentRewards.all()
    
    @classmethod
    def get_by_id(cls, student_id):
        return StudentRewards.query.filter_by(student_id=student_id).all()

    @classmethod
    def get_all_from_prize(cls, reward_id):
        return StudentRewards.query.filter_by(reward_id=reward_id).all()

    @classmethod
    def get_from_student_and_prize(cls, student_id, reward_id):
        return StudentRewards.query.filter_by(student_id=student_id,reward_id=reward_id).all()
    
    @classmethod
    def get_by_external_id(cls, external_id):
        return StudentRewards.query.filter_by(external_id=external_id).all()
    
    @classmethod
    def get_by_student_id_not_acquired(cls,student_id):
          return StudentRewards.query.filter_by(student_id=student_id, acquired = False).all()

    @classmethod
    def get_by_student_id_acquired(cls,student_id):
          return StudentRewards.query.filter_by(student_id=student_id, acquired = True).all()

    