from .general_controller import GeneralController
from ..service import employees_service


class EmployeesController(GeneralController):
    _service = employees_service
