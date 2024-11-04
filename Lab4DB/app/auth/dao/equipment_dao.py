from .general_dao import GeneralDAO
from ..domain.equipment import Equipment

class EquipmentDAO(GeneralDAO):
    _domain_type = Equipment
