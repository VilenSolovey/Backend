from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db

class RequestIssueType(db.Model):
    __tablename__ = 'request_issue_type'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(45), nullable=False)

    def __repr__(self) -> str:
        return f"RequestIssueType({self.id}, type='{self.type}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'type': self.type,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> RequestIssueType:
        return RequestIssueType(
            type=dto_dict.get('type'),
        )
