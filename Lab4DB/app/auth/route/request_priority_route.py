from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import RequestPriority
from Lab4DB.app.auth.controller import request_priority_controller
from flasgger import swag_from

requestpriority_bp = Blueprint('requestpriority', __name__, url_prefix='/requestpriority')


@requestpriority_bp.get('')
@swag_from({
    'tags': ['RequestPriority'],
    'summary': 'Get all request priorities',
    'description': 'Returns a list of all request priorities from the database',
    'responses': {
        200: {
            'description': 'List of request priorities',
            'examples': {
                'application/json': [
                    {"id": 1, "level": "Low"},
                    {"id": 2, "level": "High"}
                ]
            }
        }
    }
})
def get_all_requestpriority() -> Response:
    return make_response(jsonify(request_priority_controller.find_all()), HTTPStatus.OK)


@requestpriority_bp.post('')
@swag_from({
    'tags': ['RequestPriority'],
    'summary': 'Create a new request priority',
    'description': 'Creates a new priority level for requests',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'level': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Request priority created',
            'examples': {
                'application/json': {"id": 1, "level": "Critical"}
            }
        }
    }
})
def create_request() -> Response:
    content = request.get_json()
    request_obj = RequestPriority.create_from_dto(content)
    request_priority_controller.create(request_obj)
    return make_response(jsonify(request_obj.put_into_dto()), HTTPStatus.CREATED)


@requestpriority_bp.get('/<int:request_priority_id>')
@swag_from({
    'tags': ['RequestPriority'],
    'summary': 'Get request priority by ID',
    'parameters': [
        {'name': 'request_priority_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {
            'description': 'Request priority found',
            'examples': {
                'application/json': {"id": 1, "level": "Medium"}
            }
        },
        404: {'description': 'Request priority not found'}
    }
})
def get_request(request_priority_id: int) -> Response:
    return make_response(jsonify(request_priority_controller.find_by_id(request_priority_id)), HTTPStatus.OK)


@requestpriority_bp.put('/<int:request_priority_id>')
@swag_from({
    'tags': ['RequestPriority'],
    'summary': 'Update request priority',
    'parameters': [
        {'name': 'request_priority_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {'properties': {'level': {'type': 'string'}}}
        }
    ],
    'responses': {
        200: {'description': 'Request priority updated'}
    }
})
def update_request(request_priority_id: int) -> Response:
    content = request.get_json()
    request_obj = RequestPriority.create_from_dto(content)
    request_priority_controller.update(request_priority_id, request_obj)
    return make_response("Request updated", HTTPStatus.OK)


@requestpriority_bp.patch('/<int:request_priority_id>')
@swag_from({
    'tags': ['RequestPriority'],
    'summary': 'Patch request priority',
    'parameters': [
        {'name': 'request_priority_id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'body', 'in': 'body', 'schema': {'type': 'object'}}
    ],
    'responses': {
        200: {'description': 'Request priority patched'}
    }
})
def patch_request(request_priority_id: int) -> Response:
    content = request.get_json()
    request_priority_controller.patch(request_priority_id, content)
    return make_response("Request updated", HTTPStatus.OK)


@requestpriority_bp.delete('/<int:request_priority_id>')
@swag_from({
    'tags': ['RequestPriority'],
    'summary': 'Delete request priority',
    'parameters': [
        {'name': 'request_priority_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Request priority deleted'},
        404: {'description': 'Request priority not found'}
    }
})
def delete_request(request_priority_id: int) -> Response:
    request_priority_controller.delete(request_priority_id)
    return make_response("Request deleted", HTTPStatus.OK)
