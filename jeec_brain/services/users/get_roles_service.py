from jeec_brain.models.enums.roles_enum import RolesEnum


class GetRolesService:
    def call():
        return dir(RolesEnum)[4:]
