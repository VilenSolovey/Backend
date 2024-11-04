from .general_dao import GeneralDAO
from ..domain.software_updates import SoftwareUpdates

class SoftwareUpdatesDAO(GeneralDAO):
    _domain_type = SoftwareUpdates
