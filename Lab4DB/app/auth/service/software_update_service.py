from .general_service import GeneralService
from ..dao import software_updates_dao

class SoftwareUpdatesService(GeneralService):
    _dao = software_updates_dao
