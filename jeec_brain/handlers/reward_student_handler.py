from jeec_brain.services.students.add_reward_to_student_service import AddStudentRewardService
from jeec_brain.services.students.update_reward_to_student_service import UpdateStudentRewardService
from jeec_brain.services.students.remove_reward_to_student_service import RemoveStudentRewardService
from jeec_brain.models.reward_student import StudentRewards
class StudentRewardsHandler:
    @classmethod
    def add_reward_student(cls,student,reward):
        return AddStudentRewardService(student_id=student, reward_id = reward, acquired = False).call()

    @classmethod
    def update_reward_student(cls,student_reward, **kwargs):
        return UpdateStudentRewardService(student_reward=student_reward,kwargs=kwargs).call()

    @classmethod
    def remove_reward_student(cls,student_reward):
        return RemoveStudentRewardService(student_reward=student_reward).call()