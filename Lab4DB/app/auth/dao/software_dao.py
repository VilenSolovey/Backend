from .general_dao import GeneralDAO
from ..domain.software import Software

class SoftwareDAO(GeneralDAO):
    _domain_type = Software
