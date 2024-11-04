from .general_controller import GeneralController
from ..service import requests_has_employees_service


class RequestsHasEmployeesController(GeneralController):
    _service = requests_has_employees_service
