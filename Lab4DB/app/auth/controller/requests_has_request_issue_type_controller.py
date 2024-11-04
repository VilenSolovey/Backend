from .general_controller import GeneralController
from ..service import requests_has_request_issue_type_service


class RequestsHasRequestIssueTypeController(GeneralController):
    _service = requests_has_request_issue_type_service
