from .requests_service import RequestsService
from .request_status_service import RequestStatusService
from .request_priority_service import RequestPriorityService
from .employees_service import EmployeesService
from .equipment_service import EquipmentService
from .equipment_changes_service import EquipmentChangesService
from .locations_service import LocationsService
from .software_services import SoftwareService
from .software_issue_service import SoftwareIssuesService
from .software_update_service import SoftwareUpdatesService
from .request_has_employees_service import RequestsHasEmployeesService
from .requests_has_request_issue_type_service import RequestsHasRequestIssueTypeService
from .request_issue_type_service import RequestIssueTypeService

requests_service = RequestsService()
request_status_service = RequestStatusService()
request_priority_service = RequestPriorityService()
employees_service = EmployeesService()
equipment_service = EquipmentService()
equipment_changes_service = EquipmentChangesService()
locations_service = LocationsService()
software_service = SoftwareService()
software_issues_service = SoftwareIssuesService()
software_updates_service = SoftwareUpdatesService()
requests_has_employees_service = RequestsHasEmployeesService()
requests_has_request_issue_type_service = RequestsHasRequestIssueTypeService()
request_issue_type_service = RequestIssueTypeService()
