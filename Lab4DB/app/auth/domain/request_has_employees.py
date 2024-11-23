from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db

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
