from .general_dao import GeneralDAO
from ..domain.request_issue_type import RequestIssueType

class RequestIssueTypeDAO(GeneralDAO):
    _domain_type = RequestIssueType
