from .general_service import GeneralService
from ..dao import requests_dao

class RequestsService(GeneralService):
    _dao = requests_dao
