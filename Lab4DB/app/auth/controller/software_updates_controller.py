from .general_controller import GeneralController
from ..service import software_updates_service


class SoftwareUpdatesController(GeneralController):
    _service = software_updates_service
