from .general_service import GeneralService
from ..dao import employees_dao

class EmployeesService(GeneralService):
    _dao = employees_dao
