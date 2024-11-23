from .general_controller import GeneralController
from ..service import equipment_changes_service


class EquipmentChangesController(GeneralController):
    _service = equipment_changes_service