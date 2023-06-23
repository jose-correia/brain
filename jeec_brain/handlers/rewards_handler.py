# SERVICES
from flask import current_app
from jeec_brain.services.rewards.create_jeecpot_reward_service import (
    CreateJeecpotRewardService,
)
from jeec_brain.services.rewards.update_jeecpot_reward_service import (
    UpdateJeecpotRewardService,
)
from jeec_brain.services.rewards.delete_jeecpot_reward_service import (
    DeleteJeecpotRewardService,
)
from jeec_brain.services.rewards.create_reward_service import CreateRewardService
from jeec_brain.services.rewards.update_reward_service import UpdateRewardService
from jeec_brain.services.rewards.delete_reward_service import DeleteRewardService
from jeec_brain.services.rewards.create_squad_reward_service import (
    CreateSquadRewardService,
)
from jeec_brain.services.rewards.update_squad_reward_service import (
    UpdateSquadRewardService,
)
from jeec_brain.services.rewards.delete_squad_reward_service import (
    DeleteSquadRewardService,
)
from jeec_brain.services.files.upload_image_service import UploadImageService
from jeec_brain.services.files.delete_image_service import DeleteImageService
from jeec_brain.services.files.find_image_service import FindImageService
from jeec_brain.services.files.get_file_service import GetFileImage


class RewardsHandler:
    @classmethod
    def create_reward(cls, **kwargs):
        return CreateRewardService(kwargs=kwargs).call()

    @classmethod
    def update_reward(cls, reward, **kwargs):
        return UpdateRewardService(reward, kwargs).call()

    @classmethod
    def delete_reward(cls, reward):
        for extension in current_app.config["ALLOWED_IMAGES"]:
            image_filename = (
                str(reward.external_id).lower().replace(" ", "_") + "." + extension
            )
            DeleteImageService(image_filename, "static/rewards").call()

        return DeleteRewardService(reward).call()

    @staticmethod
    def upload_reward_image(file, reward_name):
        return UploadImageService(file, reward_name, "static/rewards").call()
    
    @staticmethod
    def get_image_reward(reward_name):
        return GetFileImage(reward_name, "static/rewards").call()

    @staticmethod
    def find_reward_image(reward_name):
        return FindImageService(reward_name, "static/rewards").call()

    @classmethod
    def create_squad_reward(cls, **kwargs):
        return CreateSquadRewardService(kwargs=kwargs).call()

    @classmethod
    def update_squad_reward(cls, squad_reward, **kwargs):
        return UpdateSquadRewardService(squad_reward, kwargs).call()

    @classmethod
    def delete_squad_reward(cls, squad_reward):
        return DeleteSquadRewardService(squad_reward).call()

    @classmethod
    def create_jeecpot_reward(cls, **kwargs):
        return CreateJeecpotRewardService(kwargs=kwargs).call()

    @classmethod
    def update_jeecpot_reward(cls, jeecpot_reward, **kwargs):
        return UpdateJeecpotRewardService(jeecpot_reward, kwargs).call()

    @classmethod
    def delete_jeecpot_reward(cls, jeecpot_reward):
        return DeleteJeecpotRewardService(jeecpot_reward).call()
