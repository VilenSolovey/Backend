from .general_service import GeneralService
from ..dao import locations_dao

class LocationsService(GeneralService):
    _dao = locations_dao
