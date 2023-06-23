from jeec_brain.models.reward_student import StudentRewards


class RemoveStudentRewardService(object):
    def __init__(self, student_reward: StudentRewards):
        self.student_reward = student_reward

    def call(self) -> bool:
        result = self.student_reward.delete()
        return result


