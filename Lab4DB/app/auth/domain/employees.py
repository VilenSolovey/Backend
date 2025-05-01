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

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Employees:

        return Employees(
            first_name=dto_dict.get('first_name'),
            last_name=dto_dict.get('last_name'),
            position=dto_dict.get('position'),
            email=dto_dict.get('email'),
            phone_number=dto_dict.get('phone_number'),
            middle_name=dto_dict.get('middle_name'),
        )

def insert_employees(n: int):
    employees = [
        Employees(
            first_name=f"Noname{i}",
            last_name=f"Lastname{i}",
            position=f"Position{i}",
            email=f"noname{i}@example.com",
            phone_number=f"123-456-789{i}",
            middle_name=f"MiddleName{i}"
        )
        for i in range(n)
    ]

    try:
        db.session.bulk_save_objects(employees)
        db.session.commit()
        return employees
    except Exception:
        db.session.rollback()
        return -1

