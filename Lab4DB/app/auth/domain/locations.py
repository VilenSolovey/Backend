from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db

class Locations(db.Model):
    __tablename__ = 'Locations'

    id = db.Column(db.Integer, primary_key=True)
    room_numbers = db.Column(db.Integer, nullable=True)
    office_name = db.Column(db.String(100), nullable=True)
    workplace_number = db.Column(db.Integer, nullable=True)

    requests = db.relationship('Requests', backref='location', lazy='dynamic')
    softwares = db.relationship('Software', back_populates='location')

    def __repr__(self) -> str:
        return f"Locations({self.id}, office_name='{self.office_name}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'room_numbers': self.room_numbers,
            'office_name': self.office_name,
            'workplace_number': self.workplace_number,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Locations:
        return Locations(
            room_numbers=dto_dict.get('room_numbers'),
            office_name=dto_dict.get('office_name'),
            workplace_number=dto_dict.get('workplace_number'),
        )
