from typing import Dict, Optional
from jeec_brain.models.users import Users


class UpdateUserService():
    
    def __init__(self, user: Users, kwargs: Dict):
        self.user = user
        self.kwargs = kwargs

    def call(self) -> Optional[Users]:
        try:
            update_result = self.user.update(**self.kwargs)
        except:
            return None
            
        return update_result
