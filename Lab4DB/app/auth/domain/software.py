from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db

class Software(db.Model):
    __tablename__ = 'Software'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    version = db.Column(db.String(45), nullable=True)
    locations_id = db.Column(db.Integer, db.ForeignKey('Locations.id'), nullable=True)

    location = db.relationship('Locations', back_populates='softwares')
    issues = db.relationship('SoftwareIssues', back_populates='software', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"Software({self.id}, name='{self.name}', version='{self.version}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'version': self.version,
            'locations_id': self.locations_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Software:
        return Software(
            name=dto_dict.get('name'),
            version=dto_dict.get('version'),
            locations_id=dto_dict.get('locations_id'),
        )
