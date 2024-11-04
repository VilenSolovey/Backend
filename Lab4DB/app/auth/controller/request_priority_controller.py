from .general_controller import GeneralController
from ..service import request_priority_service


class RequestPriorityController(GeneralController):
    _service = request_priority_service
