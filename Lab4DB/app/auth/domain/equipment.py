from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db

class Equipment(db.Model):
    __tablename__ = 'Equipment'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(45), nullable=False)
    type = db.Column(db.String(45), nullable=False)
    serial_number = db.Column(db.Integer, nullable=True)
    end_of_warranty = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"Equipment({self.id}, model='{self.model}', type='{self.type}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'model': self.model,
            'type': self.type,
            'serial_number': self.serial_number,
            'end_of_warranty': self.end_of_warranty,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Equipment:
        return Equipment(
            model=dto_dict.get('model'),
            type=dto_dict.get('type'),
            serial_number=dto_dict.get('serial_number'),
            end_of_warranty=dto_dict.get('end_of_warranty'),
        )

def insert_equipment(model: str, type: str, serial_number: int = None, end_of_warranty: str = None) -> Equipment:
    """
    Helper function to insert a new equipment into the database.
    :return: Equipment object
    """
    new_equipment = Equipment(model=model, type=type, serial_number=serial_number, end_of_warranty=end_of_warranty)
    db.session.add(new_equipment)
    db.session.commit()
    return new_equipment
