from .general_controller import GeneralController
from ..service import software_issues_service


class SoftwareIssuesController(GeneralController):
    _service = software_issues_service
