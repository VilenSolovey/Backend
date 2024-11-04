from .general_controller import GeneralController
from ..service import locations_service


class LocationsController(GeneralController):
    _service = locations_service
