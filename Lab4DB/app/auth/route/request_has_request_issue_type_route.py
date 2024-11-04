from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import RequestsHasRequestIssueType
from Lab4DB.app.auth.controller import requests_has_request_issue_type_controller

requestshasrequestissuetype_bp = Blueprint('requestshasrequestissuetype', __name__, url_prefix='/requestshasrequestissuetype')


@requestshasrequestissuetype_bp.get('')
def get_all_requestshasrequestissuetype() -> Response:
    """
    Gets all entries from the Requests_has_Request_Issue_Type table.
    :return: Response object
    """
    return make_response(jsonify(requests_has_request_issue_type_controller.find_all()), HTTPStatus.OK)


@requestshasrequestissuetype_bp.post('')
def create_requesthasrequestissuetype() -> Response:
    """
    Creates a new entry in the Requests_has_Request_Issue_Type table.
    :return: Response object
    """
    content = request.get_json()
    requesthasrequestissuetype_obj = RequestsHasRequestIssueType.create_from_dto(content)
    requests_has_request_issue_type_controller.create(requesthasrequestissuetype_obj)
    return make_response(jsonify(requesthasrequestissuetype_obj.put_into_dto()), HTTPStatus.CREATED)


@requestshasrequestissuetype_bp.get('/<int:requesthasrequestissuetype_id>')
def get_requesthasrequestissuetype(requesthasrequestissuetype_id: int) -> Response:
    """
    Gets an entry by ID.
    :return: Response object
    """
    return make_response(jsonify(requests_has_request_issue_type_controller.find_by_id(requesthasrequestissuetype_id)), HTTPStatus.OK)


@requestshasrequestissuetype_bp.delete('/<int:requesthasrequestissuetype_id>')
def delete_requesthasrequestissuetype(requesthasrequestissuetype_id: int) -> Response:
    """
    Deletes an entry by ID.
    :return: Response object
    """
    requests_has_request_issue_type_controller.delete(requesthasrequestissuetype_id)
    return make_response("Entry deleted", HTTPStatus.OK)
