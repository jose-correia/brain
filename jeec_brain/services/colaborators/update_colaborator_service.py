from typing import Dict, Optional
from jeec_brain.models.colaborators import Colaborators


class UpdateColaboratorService():
    
    def __init__(self, colaborator: Colaborators, kwargs: Dict):
        self.colaborator = colaborator
        self.kwargs = kwargs

    def call(self) -> Optional[Colaborators]:
        update_result = self.colaborator.update(**self.kwargs)
        return update_result
