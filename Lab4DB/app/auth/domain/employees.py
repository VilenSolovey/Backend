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

    requests_has_employee = db.relationship('Requests', secondary='requests_has_employees', back_populates='employees_has_requests')

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
