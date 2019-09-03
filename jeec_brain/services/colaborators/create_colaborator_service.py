from jeec_brain.models.colaborators import Colaborators

class CreateColaboratorervice(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self):
        colaborator = Colaborators(**self.kwargs)
        
        colaborator.create()
        colaborator.reload()
        
        return colaborator