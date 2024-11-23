from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db

class RequestPriority(db.Model):
    __tablename__ = 'RequestPriority'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(45), nullable=False)

    def __repr__(self) -> str:
        return f"RequestPriority({self.id}, level='{self.level}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'level': self.level,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> RequestPriority:
        return RequestPriority(
            level=dto_dict.get('level'),
        )
