from .general_dao import GeneralDAO
from ..domain.equipment_changes import EquipmentChanges

class EquipmentChangesDAO(GeneralDAO):
    _domain_type = EquipmentChanges
