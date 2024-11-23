from .general_service import GeneralService
from ..dao import request_issue_type_dao

class RequestIssueTypeService(GeneralService):
    _dao = request_issue_type_dao
