from .general_controller import GeneralController
from ..service import equipment_service


class EquipmentController(GeneralController):
    _service = equipment_service
