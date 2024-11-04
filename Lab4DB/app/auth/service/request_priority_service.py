from .general_service import GeneralService
from ..dao import request_priority_dao

class RequestPriorityService(GeneralService):
    _dao = request_priority_dao
