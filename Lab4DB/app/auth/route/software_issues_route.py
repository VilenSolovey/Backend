from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import SoftwareIssues
from Lab4DB.app.auth.controller import software_issues_controller
from flasgger import swag_from

softwareissues_bp = Blueprint('softwareissues', __name__, url_prefix='/softwareissues')


@softwareissues_bp.get('')
@swag_from({
    'tags': ['Software Issues'],
    'summary': 'Get all software issues',
    'description': 'Returns a list of all software issues from the SoftwareIssues table',
    'responses': {
        200: {
            'description': 'List of software issues',
            'examples': {
                'application/json': [
                    {"id": 1, "description": "Bug in module X", "severity": "High"},
                    {"id": 2, "description": "Memory leak in Y", "severity": "Critical"}
                ]
            }
        }
    }
})
def get_all_softwareissues() -> Response:
    return make_response(jsonify(software_issues_controller.find_all()), HTTPStatus.OK)


@softwareissues_bp.post('')
@swag_from({
    'tags': ['Software Issues'],
    'summary': 'Create a new software issue',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'SoftwareIssue',
                'properties': {
                    'description': {'type': 'string'},
                    'severity': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Software issue created'},
        400: {'description': 'Invalid input'}
    }
})
def create_softwareissue() -> Response:
    content = request.get_json()
    softwareissue_obj = SoftwareIssues.create_from_dto(content)
    software_issues_controller.create(softwareissue_obj)
    return make_response(jsonify(softwareissue_obj.put_into_dto()), HTTPStatus.CREATED)


@softwareissues_bp.get('/<int:softwareissue_id>')
@swag_from({
    'tags': ['Software Issues'],
    'summary': 'Get software issue by ID',
    'parameters': [
        {'name': 'softwareissue_id', 'in': 'path', 'required': True, 'type': 'integer'}
    ],
    'responses': {
        200: {'description': 'Software issue found'},
        404: {'description': 'Software issue not found'}
    }
})
def get_softwareissue(softwareissue_id: int) -> Response:
    return make_response(jsonify(software_issues_controller.find_by_id(softwareissue_id)), HTTPStatus.OK)


@softwareissues_bp.put('/<int:softwareissue_id>')
@swag_from({
    'tags': ['Software Issues'],
    'summary': 'Update software issue',
    'parameters': [
        {'name': 'softwareissue_id', 'in': 'path', 'required': True, 'type': 'integer'},
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'type': 'object'}}
    ],
    'responses': {
        200: {'description': 'Software issue updated'}
    }
})
def update_softwareissue(softwareissue_id: int) -> Response:
    content = request.get_json()
    softwareissue_obj = SoftwareIssues.create_from_dto(content)
    software_issues_controller.update(softwareissue_id, softwareissue_obj)
    return make_response("Software issue updated", HTTPStatus.OK)


@softwareissues_bp.patch('/<int:softwareissue_id>')
@swag_from({
    'tags': ['Software Issues'],
    'summary': 'Patch software issue',
    'parameters': [
        {'name': 'softwareissue_id', 'in': 'path', 'required': True, 'type': 'integer'},
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'type': 'object'}}
    ],
    'responses': {
        200: {'description': 'Software issue patched'}
    }
})
def patch_softwareissue(softwareissue_id: int) -> Response:
    content = request.get_json()
    software_issues_controller.patch(softwareissue_id, content)
    return make_response("Software issue patched", HTTPStatus.OK)


@softwareissues_bp.delete('/<int:softwareissue_id>')
@swag_from({
    'tags': ['Software Issues'],
    'summary': 'Delete software issue',
    'parameters': [
        {'name': 'softwareissue_id', 'in': 'path', 'required': True, 'type': 'integer'}
    ],
    'responses': {
        200: {'description': 'Software issue deleted'},
        404: {'description': 'Software issue not found'}
    }
})
def delete_softwareissue(softwareissue_id: int) -> Response:
    software_issues_controller.delete(softwareissue_id)
    return make_response("Software issue deleted", HTTPStatus.OK)
