from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import RequestsHasRequestIssueType
from Lab4DB.app.auth.controller import requests_has_request_issue_type_controller
from flasgger import swag_from

requestshasrequestissuetype_bp = Blueprint('requestshasrequestissuetype', __name__, url_prefix='/requestshasrequestissuetype')


@requestshasrequestissuetype_bp.get('')
@swag_from({
    'tags': ['Requests_has_Request_Issue_Type'],
    'summary': 'Get all relations',
    'description': 'Returns all entries from the Requests_has_Request_Issue_Type table',
    'responses': {
        200: {
            'description': 'List of relations',
            'examples': {
                'application/json': [
                    {"requests_id": 1, "request_issue_type_id": 2},
                    {"requests_id": 2, "request_issue_type_id": 3}
                ]
            }
        }
    }
})
def get_all_requestshasrequestissuetype() -> Response:
    return make_response(jsonify(requests_has_request_issue_type_controller.find_all()), HTTPStatus.OK)


@requestshasrequestissuetype_bp.post('')
@swag_from({
    'tags': ['Requests_has_Request_Issue_Type'],
    'summary': 'Create a new relation',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'requests_id': {'type': 'integer'},
                    'request_issue_type_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Relation created',
            'examples': {
                'application/json': {"requests_id": 1, "request_issue_type_id": 2}
            }
        }
    }
})
def create_requesthasrequestissuetype() -> Response:
    content = request.get_json()
    requesthasrequestissuetype_obj = RequestsHasRequestIssueType.create_from_dto(content)
    requests_has_request_issue_type_controller.create(requesthasrequestissuetype_obj)
    return make_response(jsonify(requesthasrequestissuetype_obj.put_into_dto()), HTTPStatus.CREATED)


@requestshasrequestissuetype_bp.get('/<int:requesthasrequestissuetype_id>')
@swag_from({
    'tags': ['Requests_has_Request_Issue_Type'],
    'summary': 'Get relation by ID',
    'parameters': [
        {'name': 'requesthasrequestissuetype_id', 'in': 'path', 'required': True, 'type': 'integer'}
    ],
    'responses': {
        200: {'description': 'Relation found'},
        404: {'description': 'Relation not found'}
    }
})
def get_requesthasrequestissuetype(requesthasrequestissuetype_id: int) -> Response:
    return make_response(jsonify(requests_has_request_issue_type_controller.find_by_id(requesthasrequestissuetype_id)), HTTPStatus.OK)


@requestshasrequestissuetype_bp.delete('/<int:requests_id>/<int:issue_type_id>')
@swag_from({
    'tags': ['Requests_has_Request_Issue_Type'],
    'summary': 'Delete relation',
    'parameters': [
        {'name': 'requests_id', 'in': 'path', 'required': True, 'type': 'integer'},
        {'name': 'issue_type_id', 'in': 'path', 'required': True, 'type': 'integer'}
    ],
    'responses': {
        200: {'description': 'Relation deleted'},
        404: {'description': 'Relation not found'}
    }
})
def delete_requesthasrequestissuetype(requests_id: int, issue_type_id: int) -> Response:
    requests_has_request_issue_type_controller.delete(requests_id, issue_type_id)
    return make_response("Entry deleted", HTTPStatus.OK)


@requestshasrequestissuetype_bp.put('/<int:requests_id>/<int:request_issue_type_id>')
@swag_from({
    'tags': ['Requests_has_Request_Issue_Type'],
    'summary': 'Update relation',
    'description': 'Updates an existing Requests_has_Request_Issue_Type entry',
    'parameters': [
        {'name': 'requests_id', 'in': 'path', 'required': True, 'type': 'integer'},
        {'name': 'request_issue_type_id', 'in': 'path', 'required': True, 'type': 'integer'},
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'type': 'object'}}
    ],
    'responses': {
        200: {'description': 'Relation updated'}
    }
})
def update_requesthasrequestissuetype(requests_id: int, request_issue_type_id: int) -> Response:
    content = request.get_json()
    new_obj = RequestsHasRequestIssueType.create_from_dto(content)
    requests_has_request_issue_type_controller.update(requests_id, request_issue_type_id, new_obj)
    return make_response(jsonify(new_obj.put_into_dto()), HTTPStatus.OK)


