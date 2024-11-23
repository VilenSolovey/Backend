from .general_controller import GeneralController
from ..service import requests_has_request_issue_type_service
from Lab4DB.app.auth.domain import RequestsHasRequestIssueType
from Lab4DB.app import db

class RequestsHasRequestIssueTypeController(GeneralController):
    _service = requests_has_request_issue_type_service

    def find_by_ids(self, requests_id: int, request_issue_type_id: int) -> RequestsHasRequestIssueType:
        return db.session.query(RequestsHasRequestIssueType).filter_by(
            requests_id=requests_id,
            request_issue_type_id=request_issue_type_id
        ).first()

    def update(self, requests_id: int, request_issue_type_id: int, new_obj: RequestsHasRequestIssueType) -> None:

        obj = self.find_by_ids(requests_id, request_issue_type_id)


        if obj is None:
            raise ValueError("Об'єкт з вказаними ID не знайдено")


        obj.requests_id = new_obj.requests_id
        obj.request_issue_type_id = new_obj.request_issue_type_id

        db.session.commit()

    