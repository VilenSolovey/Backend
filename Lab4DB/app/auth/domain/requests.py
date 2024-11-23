from __future__ import annotations
from typing import Dict, Any
from Lab4DB.app import db

class Requests(db.Model):
    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    creation_time = db.Column(db.DateTime, nullable=False)

    requeststatusid = db.Column(db.Integer, db.ForeignKey('requeststatus.id'))
    request_priority_id = db.Column(db.Integer, db.ForeignKey('RequestPriority.id'))
    locations_id = db.Column(db.Integer, db.ForeignKey('Locations.id'))

    software_updates = db.relationship('SoftwareUpdates', back_populates='request')

    def __repr__(self) -> str:
        return f"Requests({self.id}, description='{self.description}', creation_time='{self.creation_time}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'description': self.description,
            'creation_time': self.creation_time,
            'requeststatus': self.requeststatusid,
            'request_priority_id': self.request_priority_id,
            'locations_id': self.locations_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Requests:
        request = Requests(
            description=dto_dict.get('description'),
            creation_time=dto_dict.get('creation_time'),
            requeststatusid=dto_dict.get('requeststatusid'),
            request_priority_id=dto_dict.get('request_priority_id'),
            locations_id=dto_dict.get('locations_id'),
        )
        return request
