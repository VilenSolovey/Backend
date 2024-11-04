from .general_service import GeneralService
from ..dao import equipment_changes_dao

class EquipmentChangesService(GeneralService):
    _dao = equipment_changes_dao
