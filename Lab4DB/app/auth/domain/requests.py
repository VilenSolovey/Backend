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
    employees_has_requests = db.relationship('Employees', secondary='requests_has_employees',
                                             back_populates='requests_has_employee')
    requests_has_issue = db.relationship('RequestIssueType', secondary='requests_has_request_issue_type',
                                         back_populates='requests_has_issue')

    def __repr__(self) -> str:
        return f"Requests({self.id}, description='{self.description}', creation_time='{self.creation_time}')"

    def put_into_dto(self) -> Dict[str, Any]:
        requests_employees_dto = [
            {
                'employee': employee.put_into_dto(),
                'request': {'id': self.id, 'description': self.description}
            }
            for employee in self.employees_has_requests
        ]

        requests_issue_types_dto = [
            {
                'issue_type': issue_type.put_into_dto(),
                'request': {'id': self.id, 'description': self.description}
            }
            for issue_type in self.requests_has_issue
        ]

        return {
            'id': self.id,
            'description': self.description,
            'creation_time': self.creation_time,
            'requeststatus': self.requeststatusid,
            'request_priority_id': self.request_priority_id,
            'locations_id': self.locations_id,
            'requests_employees': requests_employees_dto,
            'requests_issue_types': requests_issue_types_dto,
        }
