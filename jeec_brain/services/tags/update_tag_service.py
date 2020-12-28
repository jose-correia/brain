from typing import Dict, Optional
from jeec_brain.models.tags import Tags


class UpdateTagService():
    
    def __init__(self, tag: Tags, kwargs: Dict):
        self.tag = tag
        self.kwargs = kwargs

    def call(self) -> Optional[Tags]:
        try:
            update_result = self.tag.update(**self.kwargs)
        except:
            return None
            
        return update_result
