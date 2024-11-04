from .general_dao import GeneralDAO
from ..domain.software_issues import SoftwareIssues

class SoftwareIssuesDAO(GeneralDAO):
    _domain_type = SoftwareIssues
