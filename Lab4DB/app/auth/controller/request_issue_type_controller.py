from .general_controller import GeneralController
from ..service import request_issue_type_service


class RequestIssueTypeController(GeneralController):
    _service = request_issue_type_service
