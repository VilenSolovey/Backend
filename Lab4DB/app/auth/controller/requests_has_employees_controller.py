from .general_controller import GeneralController
from ..service import requests_has_employees_service
from Lab4DB.app.auth.domain import RequestsHasEmployees
from Lab4DB.app import db

class RequestsHasEmployeesController(GeneralController):
    _service = requests_has_employees_service

    def find_by_ids(self, requests_id: int, employees_id: int) -> RequestsHasEmployees:
        return db.session.query(RequestsHasEmployees).filter_by(
            requests_id=requests_id,
            employees_id=employees_id
        ).first()

    def update(self, requests_id: int, employees_id: int, new_obj: RequestsHasEmployees) -> None:
        obj = self.find_by_ids(requests_id, employees_id)

        if obj:

            obj.requests_id = new_obj.requests_id
            obj.employees_id = new_obj.employees_id
            db.session.commit()
        else:
            db.session.add(new_obj)
            db.session.commit()

    def delete(self, requests_id: int, employees_id: int) -> None:
        obj = self.find_by_ids(requests_id, employees_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
