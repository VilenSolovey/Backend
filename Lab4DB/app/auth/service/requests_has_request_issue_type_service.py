from .general_service import GeneralService
from ..dao import requests_has_request_issue_type_dao

class RequestsHasRequestIssueTypeService(GeneralService):
    _dao = requests_has_request_issue_type_dao
