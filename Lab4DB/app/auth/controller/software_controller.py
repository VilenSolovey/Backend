from .general_controller import GeneralController
from ..service import software_service


class SoftwareController(GeneralController):
    _service = software_service
