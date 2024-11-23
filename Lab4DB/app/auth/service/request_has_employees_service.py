from .general_service import GeneralService
from ..dao import requests_has_employees_dao

class RequestsHasEmployeesService(GeneralService):
    _dao = requests_has_employees_dao
