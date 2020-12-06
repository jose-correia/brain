from jeec_brain.models.tags import Tags

class CreateTagService(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def call(self):        
        tag = Tags.create(**self.kwargs)

        if not tag:
            return None

        return tag