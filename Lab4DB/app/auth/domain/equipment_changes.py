from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db

class EquipmentChanges(db.Model):
    __tablename__ = 'EquipmentChanges'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=True)
    old_equipment_id = db.Column(db.Integer, db.ForeignKey('Equipment.id'), nullable=True)
    new_equipment_id = db.Column(db.Integer, db.ForeignKey('Equipment.id'), nullable=True)
    request_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=True)

    def __repr__(self) -> str:
        return f"EquipmentChanges({self.id}, date='{self.date}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'date': self.date,
            'old_equipment_id': self.old_equipment_id,
            'new_equipment_id': self.new_equipment_id,
            'request_id': self.request_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> EquipmentChanges:
        return EquipmentChanges(
            date=dto_dict.get('date'),
            old_equipment_id=dto_dict.get('old_equipment_id'),
            new_equipment_id=dto_dict.get('new_equipment_id'),
            request_id=dto_dict.get('request_id'),
        )
