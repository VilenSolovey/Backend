from .general_dao import GeneralDAO
from ..domain.requests import Requests

class RequestsDAO(GeneralDAO):
    _domain_type = Requests
