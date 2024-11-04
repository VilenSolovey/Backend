from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db

class RequestsHasRequestIssueType(db.Model):
    __tablename__ = 'requests_has_request_issue_type'

    requests_id = db.Column(db.Integer, db.ForeignKey('requests.id'), primary_key=True)
    request_issue_type_id = db.Column(db.Integer, db.ForeignKey('request_issue_type.id'), primary_key=True)

    def __repr__(self) -> str:
        return f"RequestsHasRequestIssueType(requests_id={self.requests_id}, request_issue_type_id={self.request_issue_type_id})"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'requests_id': self.requests_id,
            'request_issue_type_id': self.request_issue_type_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> RequestsHasRequestIssueType:
        return RequestsHasRequestIssueType(
            requests_id=dto_dict.get('requests_id'),
            request_issue_type_id=dto_dict.get('request_issue_type_id'),
        )
