
from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import RequestStatus
from Lab4DB.app.auth.controller import request_status_controller
from flasgger import swag_from

requeststatus_bp = Blueprint('requeststatus', __name__, url_prefix='/requeststatus')


@requeststatus_bp.get('')
@swag_from({
    'tags': ['RequestStatus'],
    'summary': 'Get all request statuses',
    'description': 'Returns a list of all request statuses in the database',
    'responses': {
        200: {
            'description': 'A list of request statuses',
            'examples': {
                'application/json': [
                    {'id': 1, 'name': 'Open'},
                    {'id': 2, 'name': 'In Progress'},
                    {'id': 3, 'name': 'Closed'}
                ]
            }
        }
    }
})
def get_all_requeststatus() -> Response:
    return make_response(jsonify(request_status_controller.find_all()), HTTPStatus.OK)


@requeststatus_bp.post('')
@swag_from({
    'tags': ['RequestStatus'],
    'summary': 'Create a new request status',
    'description': 'Adds a new request status to the RequestStatus table',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'RequestStatus',
                'properties': {
                    'name': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Request status created',
            'examples': {
                'application/json': {'id': 1, 'name': 'Open'}
            }
        }
    }
})
def create_requeststatus() -> Response:
    content = request.get_json()
    requeststatus_obj = RequestStatus.create_from_dto(content)
    request_status_controller.create(requeststatus_obj)
    return make_response(jsonify(requeststatus_obj.put_into_dto()), HTTPStatus.CREATED)


@requeststatus_bp.put('/<int:requeststatus_id>')
@swag_from({
    'tags': ['RequestStatus'],
    'summary': 'Update request status',
    'parameters': [
        {'name': 'requeststatus_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'RequestStatus',
                'properties': {'name': {'type': 'string'}}
            }
        }
    ],
    'responses': {200: {'description': 'Request status updated'}}
})
def update_requeststatus(requeststatus_id: int) -> Response:
    content = request.get_json()
    requeststatus_obj = RequestStatus.create_from_dto(content)
    request_status_controller.update(requeststatus_id, requeststatus_obj)
    return make_response("Request status updated", HTTPStatus.OK)


@requeststatus_bp.patch('/<int:requeststatus_id>')
@swag_from({
    'tags': ['RequestStatus'],
    'summary': 'Patch request status',
    'parameters': [
        {'name': 'requeststatus_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'RequestStatusPatch',
                'properties': {'name': {'type': 'string'}}
            }
        }
    ],
    'responses': {200: {'description': 'Request status patched'}}
})
def patch_requeststatus(requeststatus_id: int) -> Response:
    content = request.get_json()
    request_status_controller.patch(requeststatus_id, content)
    return make_response("Request status patched", HTTPStatus.OK)


@requeststatus_bp.delete('/<int:requeststatus_id>')
@swag_from({
    'tags': ['RequestStatus'],
    'summary': 'Delete request status',
    'parameters': [{'name': 'requeststatus_id', 'in': 'path', 'type': 'integer', 'required': True}],
    'responses': {200: {'description': 'Request status deleted'}}
})
def delete_requeststatus(requeststatus_id: int) -> Response:
    request_status_controller.delete(requeststatus_id)
    return make_response("Request status deleted", HTTPStatus.OK)

