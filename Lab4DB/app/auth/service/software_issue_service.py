from .general_service import GeneralService
from ..dao import software_issues_dao

class SoftwareIssuesService(GeneralService):
    _dao = software_issues_dao
