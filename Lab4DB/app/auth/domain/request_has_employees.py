from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db
from .requests import Requests
from .employees import Employees
class RequestsHasEmployees(db.Model):
    __tablename__ = 'requests_has_employees'

    requests_id = db.Column(db.Integer, db.ForeignKey('requests.id'), primary_key=True)
    employees_id = db.Column(db.Integer, db.ForeignKey('employees.id'), primary_key=True)

    def __repr__(self) -> str:
        return f"RequestsHasEmployees(requests_id={self.requests_id}, employees_id={self.employees_id})"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'requests_id': self.requests_id,
            'employees_id': self.employees_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> RequestsHasEmployees:
        return RequestsHasEmployees(
            requests_id=dto_dict.get('requests_id'),
            employees_id=dto_dict.get('employees_id'),
        )

    @staticmethod
    def add_request_to_employee(description: str, first_name: str, last_name: str) -> RequestsHasEmployees:
        request = Requests.query.filter_by(description=description).first()
        if not request:
            raise ValueError(f"Request with description '{description}' not found")


        employee = Employees.query.filter_by(first_name=first_name, last_name=last_name).first()
        if not employee:
            raise ValueError(f"Employee {first_name} {last_name} not found")


        request_has_employee = RequestsHasEmployees(requests_id=request.id, employees_id=employee.id)


        db.session.add(request_has_employee)
        db.session.commit()

        return request_has_employee
