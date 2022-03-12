from jeec_brain.models.tags import Tags


class DeleteTagService:
    def __init__(self, tag: Tags):
        self.tag = tag

    def call(self) -> bool:
        result = self.tag.delete()
        return result
