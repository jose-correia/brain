from pydantic import BaseModel, Field
from uuid import UUID

class SquadRewardPath(BaseModel):
    squad_reward_external_id: UUID = Field(..., description="Squad Reward external ID")

class JeecpotRewardsPath(BaseModel):
    jeecpot_rewards_external_id: UUID = Field(..., description="Jeecpot rewards external ID")

class RewardPath(BaseModel):
    reward_external_id: UUID = Field(..., description="Reward external ID")

class TagPath(BaseModel):
    tag_external_id: UUID = Field(..., description="Tag external ID")

class LevelPath(BaseModel):
    level_external_id: UUID = Field(..., description="Level external ID")

class SquadPath(BaseModel):
    squad_external_id: UUID = Field(..., description="Squad external ID")

class StudentPath(BaseModel):
    student_external_id: UUID = Field(..., description="Student external ID")