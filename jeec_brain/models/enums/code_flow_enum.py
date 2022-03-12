import enum


class CodeFlowEnum(enum.Enum):
    AdminOneUseCode = "Admin generates code, student uses it and its deleted"
    AdminMultiUseCode = (
        "Admin generates code, multiple students use it, admin deletes it"
    )
    CompanyOneUseCode = "Company generates code, student uses it and its deleted"
    CompanyMultiUseCode = (
        "Company generates code, multiple students use it, admin deletes it"
    )
    CompanyISTID = "Company uses student IST id"
