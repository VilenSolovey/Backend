from .general_controller import GeneralController
from ..service import tasks_service


class TasksController(GeneralController):
    _service = tasks_service
