from .general_dao import GeneralDAO
from ..domain.employees import Employees


class EmployeesDAO(GeneralDAO):
    _domain_type = Employees
