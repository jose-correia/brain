from jeec_brain.models.reward_student import StudentRewards
from typing import Dict,Optional

class UpdateStudentRewardService:
    def __init__(self, student_reward: StudentRewards, kwargs: Dict):
        self.student_reward = student_reward
        self.kwargs = kwargs

    
    def call(self) -> Optional[StudentRewards]:
        try:
            update_result = self.student_reward.update(**self.kwargs)
        except:
            return None

        return update_result
