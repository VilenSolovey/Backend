from .general_dao import GeneralDAO
from ..domain.request_priority import RequestPriority

class RequestPriorityDAO(GeneralDAO):
    _domain_type = RequestPriority
