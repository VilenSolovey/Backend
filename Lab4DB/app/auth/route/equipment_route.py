from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import Equipment
from Lab4DB.app.auth.controller import equipment_controller
from ..domain.equipment import insert_equipment
from flasgger import swag_from

equipment_bp = Blueprint('equipment', __name__, url_prefix='/equipment')


@equipment_bp.get('')
@swag_from({
    'tags': ['Equipment'],
    'summary': 'Get all equipment',
    'description': 'Returns a list of all equipment from the Equipment table',
    'responses': {
        200: {
            'description': 'List of equipment',
            'examples': {
                'application/json': [
                    {"id": 1, "model": "Dell XPS", "type": "Laptop", "serial_number": 123456},
                    {"id": 2, "model": "HP LaserJet", "type": "Printer", "serial_number": 789012}
                ]
            }
        }
    }
})
def get_all_equipment() -> Response:
    return make_response(jsonify(equipment_controller.find_all()), HTTPStatus.OK)


@equipment_bp.post('')
@swag_from({
    'tags': ['Equipment'],
    'summary': 'Create new equipment',
    'description': 'Creates a new equipment entry in the database',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'model': {'type': 'string'},
                    'type': {'type': 'string'},
                    'serial_number': {'type': 'integer'},
                    'end_of_warranty': {'type': 'string', 'format': 'date-time'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Equipment created',
            'examples': {
                'application/json': {"id": 1, "model": "Dell XPS", "type": "Laptop"}
            }
        }
    }
})
def create_equipment() -> Response:
    content = request.get_json()
    equipment_obj = Equipment.create_from_dto(content)
    equipment_controller.create(equipment_obj)
    return make_response(jsonify(equipment_obj.put_into_dto()), HTTPStatus.CREATED)


@equipment_bp.get('/<int:equipment_id>')
@swag_from({
    'tags': ['Equipment'],
    'summary': 'Get equipment by ID',
    'parameters': [
        {'name': 'equipment_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Equipment found'},
        404: {'description': 'Equipment not found'}
    }
})
def get_equipment(equipment_id: int) -> Response:
    return make_response(jsonify(equipment_controller.find_by_id(equipment_id)), HTTPStatus.OK)


@equipment_bp.put('/<int:equipment_id>')
@swag_from({
    'tags': ['Equipment'],
    'summary': 'Update equipment',
    'parameters': [
        {'name': 'equipment_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'model': {'type': 'string'},
                    'type': {'type': 'string'},
                    'serial_number': {'type': 'integer'},
                    'end_of_warranty': {'type': 'string', 'format': 'date-time'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Equipment updated'}
    }
})
def update_equipment(equipment_id: int) -> Response:
    content = request.get_json()
    equipment_obj = Equipment.create_from_dto(content)
    equipment_controller.update(equipment_id, equipment_obj)
    return make_response("Equipment updated", HTTPStatus.OK)


@equipment_bp.patch('/<int:equipment_id>')
@swag_from({
    'tags': ['Equipment'],
    'summary': 'Patch equipment',
    'parameters': [
        {'name': 'equipment_id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'body', 'in': 'body', 'schema': {'type': 'object'}}
    ],
    'responses': {
        200: {'description': 'Equipment patched'}
    }
})
def patch_equipment(equipment_id: int) -> Response:
    content = request.get_json()
    equipment_controller.patch(equipment_id, content)
    return make_response("Equipment patched", HTTPStatus.OK)


@equipment_bp.delete('/<int:equipment_id>')
@swag_from({
    'tags': ['Equipment'],
    'summary': 'Delete equipment',
    'parameters': [
        {'name': 'equipment_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Equipment deleted'},
        404: {'description': 'Equipment not found'}
    }
})
def delete_equipment(equipment_id: int) -> Response:
    equipment_controller.delete(equipment_id)
    return make_response("Equipment deleted", HTTPStatus.OK)

@equipment_bp.route('/parametrized', methods=['POST'])
def create_parametrized_equipment() -> Response:
    """
    Creates a new equipment entry with parameters.
    :return: Response object
    """
    content = request.get_json()
    new_equipment = insert_equipment(
        model=content['model'],
        type=content['type'],
        serial_number=content.get('serial_number'),
        end_of_warranty=content.get('end_of_warranty')
    )
    return make_response(jsonify(new_equipment.put_into_dto()), HTTPStatus.CREATED)

