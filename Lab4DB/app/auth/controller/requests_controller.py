from .general_controller import GeneralController
from ..service import requests_service


class RequestsController(GeneralController):
    _service = requests_service
