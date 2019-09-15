# SERVICES
from jeec_brain.services.colaborators.create_colaborator_service import CreateColaboratorService
from jeec_brain.services.colaborators.update_colaborator_service import UpdateColaboratorService
from jeec_brain.services.colaborators.delete_colaborator_service import DeleteColaboratorService


class ColaboratorsHandler():

    @classmethod
    def create_colaborator(cls, **kwargs):
        return CreateColaboratorService(kwargs=kwargs).call()

    @classmethod
    def update_colaborator(cls, colaborator, **kwargs):
        return UpdateColaboratorService(colaborator=colaborator, kwargs=kwargs).call()

    @classmethod
    def delete_colaborator(cls, colaborator):
        return DeleteColaboratorService(colaborator=colaborator).call()

    # @classmethod
    # def upload_photo(file, filename):
    #     try:
    #         file.save(os.path.join(current_app.root_path, 'storage', filename))
    #         return True
    #     except Exception as e:
    #         logger.error(e)
