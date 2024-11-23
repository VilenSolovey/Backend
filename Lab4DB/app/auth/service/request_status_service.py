from .general_service import GeneralService
from ..dao import request_status_dao

class RequestStatusService(GeneralService):
    _dao = request_status_dao