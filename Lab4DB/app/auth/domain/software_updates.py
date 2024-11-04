from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db

class SoftwareUpdates(db.Model):
    __tablename__ = 'SoftwareUpdates'

    id = db.Column(db.Integer, primary_key=True)
    update_date = db.Column(db.String(45), nullable=True)
    software_id = db.Column(db.Integer, db.ForeignKey('Software.id'), nullable=True)
    requests_id = db.Column(db.Integer, db.ForeignKey('requests.id'), nullable=True)

    request = db.relationship('Requests', back_populates='software_updates')

    def __repr__(self) -> str:
        return f"SoftwareUpdates({self.id}, update_date='{self.update_date}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'update_date': self.update_date,
            'software_id': self.software_id,
            'requests_id': self.requests_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> SoftwareUpdates:
        return SoftwareUpdates(
            update_date=dto_dict.get('update_date'),
            software_id=dto_dict.get('software_id'),
            requests_id=dto_dict.get('requests_id'),
        )
