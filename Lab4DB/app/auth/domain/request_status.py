from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db

class RequestStatus(db.Model):
    __tablename__ = 'requeststatus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self) -> str:
        return f"RequestStatus({self.id}, name='{self.name}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> RequestStatus:
        return RequestStatus(
            name=dto_dict.get('name'),
        )
