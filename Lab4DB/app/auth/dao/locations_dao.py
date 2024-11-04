from .general_dao import GeneralDAO
from ..domain.locations import Locations

class LocationsDAO(GeneralDAO):
    _domain_type = Locations
