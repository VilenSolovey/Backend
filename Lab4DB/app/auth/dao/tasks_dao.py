from .general_dao import GeneralDAO
from ..domain.tasks import Tasks
class TaskDAO(GeneralDAO):
    _domain_type = Tasks