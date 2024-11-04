from .general_service import GeneralService
from ..dao import software_dao

class SoftwareService(GeneralService):
    _dao = software_dao
