from .general_service import GeneralService
from ..dao import tasks_dao
class TaskService(GeneralService):
    _dao = tasks_dao