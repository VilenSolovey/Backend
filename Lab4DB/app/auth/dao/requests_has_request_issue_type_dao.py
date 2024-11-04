from .general_dao import GeneralDAO
from ..domain.request_has_request_issue_type import RequestsHasRequestIssueType

class RequestsHasRequestIssueTypeDAO(GeneralDAO):
    _domain_type = RequestsHasRequestIssueType
