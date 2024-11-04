from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db


class Employees(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45), nullable=False)
    last_name = db.Column(db.String(45), nullable=False)
    position = db.Column(db.String(45), nullable=True)
    email = db.Column(db.String(45), nullable=True)
    phone_number = db.Column(db.String(45), nullable=True)
    middle_name = db.Column(db.String(45), nullable=True)

    requests = db.relationship('Requests', secondary='requests_has_employees', backref='requests_of_employees')

    def __repr__(self) -> str:
        return f"Employees({self.id}, first_name='{self.first_name}', last_name='{self.last_name}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'position': self.position,
            'email': self.email,
            'phone_number': self.phone_number,
            'middle_name': self.middle_name,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Employees:
        employee = Employees(
            first_name=dto_dict.get('first_name'),
            last_name=dto_dict.get('last_name'),
            position=dto_dict.get('position'),
            email=dto_dict.get('email'),
            phone_number=dto_dict.get('phone_number'),
            middle_name=dto_dict.get('middle_name'),
        )
        return employee
