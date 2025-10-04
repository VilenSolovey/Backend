from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import SoftwareUpdates
from Lab4DB.app.auth.controller import software_updates_controller
from flasgger import swag_from

softwareupdates_bp = Blueprint('softwareupdates', __name__, url_prefix='/softwareupdates')


@softwareupdates_bp.get('')
@swag_from({
    'tags': ['Software Updates'],
    'summary': 'Get all software updates',
    'description': 'Returns all software updates from the database',
    'responses': {
        200: {
            'description': 'List of software updates',
            'examples': {
                'application/json': [
                    {"id": 1, "version": "1.0.1", "description": "Security patch"},
                    {"id": 2, "version": "1.1.0", "description": "New features"}
                ]
            }
        }
    }
})
def get_all_softwareupdates() -> Response:
    return make_response(jsonify(software_updates_controller.find_all()), HTTPStatus.OK)


@softwareupdates_bp.post('')
@swag_from({
    'tags': ['Software Updates'],
    'summary': 'Create a new software update',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'SoftwareUpdate',
                'properties': {
                    'version': {'type': 'string'},
                    'description': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Software update created'},
        400: {'description': 'Invalid input'}
    }
})
def create_softwareupdate() -> Response:
    content = request.get_json()
    softwareupdate_obj = SoftwareUpdates.create_from_dto(content)
    software_updates_controller.create(softwareupdate_obj)
    return make_response(jsonify(softwareupdate_obj.put_into_dto()), HTTPStatus.CREATED)


@softwareupdates_bp.get('/<int:softwareupdate_id>')
@swag_from({
    'tags': ['Software Updates'],
    'summary': 'Get software update by ID',
    'parameters': [
        {'name': 'softwareupdate_id', 'in': 'path', 'required': True, 'type': 'integer'}
    ],
    'responses': {
        200: {'description': 'Software update found'},
        404: {'description': 'Not found'}
    }
})
def get_softwareupdate(softwareupdate_id: int) -> Response:
    return make_response(jsonify(software_updates_controller.find_by_id(softwareupdate_id)), HTTPStatus.OK)


@softwareupdates_bp.put('/<int:softwareupdate_id>')
@swag_from({
    'tags': ['Software Updates'],
    'summary': 'Update a software update',
    'parameters': [
        {'name': 'softwareupdate_id', 'in': 'path', 'required': True, 'type': 'integer'},
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'type': 'object'}}
    ],
    'responses': {
        200: {'description': 'Software update updated'}
    }
})
def update_softwareupdate(softwareupdate_id: int) -> Response:
    content = request.get_json()
    softwareupdate_obj = SoftwareUpdates.create_from_dto(content)
    software_updates_controller.update(softwareupdate_id, softwareupdate_obj)
    return make_response("Software update updated", HTTPStatus.OK)


@softwareupdates_bp.patch('/<int:softwareupdate_id>')
@swag_from({
    'tags': ['Software Updates'],
    'summary': 'Patch a software update',
    'parameters': [
        {'name': 'softwareupdate_id', 'in': 'path', 'required': True, 'type': 'integer'},
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'type': 'object'}}
    ],
    'responses': {
        200: {'description': 'Software update patched'}
    }
})
def patch_softwareupdate(softwareupdate_id: int) -> Response:
    content = request.get_json()
    software_updates_controller.patch(softwareupdate_id, content)
    return make_response("Software update patched", HTTPStatus.OK)


@softwareupdates_bp.delete('/<int:softwareupdate_id>')
@swag_from({
    'tags': ['Software Updates'],
    'summary': 'Delete software update',
    'parameters': [
        {'name': 'softwareupdate_id', 'in': 'path', 'required': True, 'type': 'integer'}
    ],
    'responses': {
        200: {'description': 'Software update deleted'},
        404: {'description': 'Not found'}
    }
})
def delete_softwareupdate(softwareupdate_id: int) -> Response:
    software_updates_controller.delete(softwareupdate_id)
    return make_response("Software update deleted", HTTPStatus.OK)

