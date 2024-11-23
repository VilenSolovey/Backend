from .general_dao import GeneralDAO
from ..domain.request_status import RequestStatus

class RequestStatusDAO(GeneralDAO):
    _domain_type = RequestStatus
