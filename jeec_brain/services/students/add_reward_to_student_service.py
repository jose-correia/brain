from jeec_brain.models.reward_student import StudentRewards


class AddStudentRewardService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self):
        student_reward = StudentRewards.create(**self.kwargs)

        if not student_reward:
            return None

        return student_reward


