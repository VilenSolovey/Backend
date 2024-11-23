from .general_service import GeneralService
from ..dao import equipment_dao

class EquipmentService(GeneralService):
    _dao = equipment_dao
