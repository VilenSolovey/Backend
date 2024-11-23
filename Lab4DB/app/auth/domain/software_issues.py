from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db
class SoftwareIssues(db.Model):
    __tablename__ = 'SoftwareIssues'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(125), nullable=True)
    software_id = db.Column(db.Integer, db.ForeignKey('Software.id'), nullable=True)

    software = db.relationship('Software', back_populates='issues')

    def __repr__(self) -> str:
        return f"SoftwareIssues({self.id}, description='{self.description}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'description': self.description,
            'software_id': self.software_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> SoftwareIssues:
        return SoftwareIssues(
            description=dto_dict.get('description'),
            software_id=dto_dict.get('software_id'),
        )
