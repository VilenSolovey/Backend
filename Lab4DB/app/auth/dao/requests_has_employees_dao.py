from .general_dao import GeneralDAO
from ..domain.request_has_employees import RequestsHasEmployees

class RequestsHasEmployeesDAO(GeneralDAO):
    _domain_type = RequestsHasEmployees
