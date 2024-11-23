from .general_controller import GeneralController
from ..service import request_status_service


class RequestStatusController(GeneralController):
    _service = request_status_service
