from .employees_dao import EmployeesDAO
from .requests_dao import RequestsDAO
from .equipment_dao import EquipmentDAO
from .equipment_changes_dao import EquipmentChangesDAO
from .locations_dao import LocationsDAO
from .request_status_dao import RequestStatusDAO
from .request_priority_dao import RequestPriorityDAO
from .request_issue_type_dao import RequestIssueTypeDAO
from .software_dao import SoftwareDAO
from .software_updates_dao import SoftwareUpdatesDAO
from .software_issues_dao import SoftwareIssuesDAO
from .requests_has_employees_dao import RequestsHasEmployeesDAO
from .requests_has_request_issue_type_dao import RequestsHasRequestIssueTypeDAO

employees_dao = EmployeesDAO()
requests_dao = RequestsDAO()
equipment_dao = EquipmentDAO()
equipment_changes_dao = EquipmentChangesDAO()
locations_dao = LocationsDAO()
request_status_dao = RequestStatusDAO()
request_priority_dao = RequestPriorityDAO()
request_issue_type_dao = RequestIssueTypeDAO()
software_dao = SoftwareDAO()
software_updates_dao = SoftwareUpdatesDAO()
software_issues_dao = SoftwareIssuesDAO()
requests_has_employees_dao = RequestsHasEmployeesDAO()
requests_has_request_issue_type_dao = RequestsHasRequestIssueTypeDAO()
