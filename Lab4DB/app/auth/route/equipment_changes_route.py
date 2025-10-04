from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import EquipmentChanges
from Lab4DB.app.auth.controller import equipment_changes_controller
from flasgger import swag_from

equipmentchanges_bp = Blueprint('equipmentchanges', __name__, url_prefix='/equipmentchanges')


@equipmentchanges_bp.get('')
@swag_from({
    'tags': ['EquipmentChanges'],
    'summary': 'Get all equipment changes',
    'description': 'Returns a list of all equipment changes in the database',
    'responses': {
        200: {
            'description': 'A list of equipment changes',
            'examples': {
                'application/json': [
                    {'id': 1, 'equipment_id': 5, 'change': 'Replaced battery', 'date': '2025-09-28'}
                ]
            }
        }
    }
})
def get_all_equipmentchanges() -> Response:
    return make_response(jsonify(equipment_changes_controller.find_all()), HTTPStatus.OK)


@equipmentchanges_bp.post('')
@swag_from({
    'tags': ['EquipmentChanges'],
    'summary': 'Create a new equipment change',
    'description': 'Adds a new entry to the EquipmentChanges table',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'EquipmentChange',
                'properties': {
                    'equipment_id': {'type': 'integer'},
                    'change': {'type': 'string'},
                    'date': {'type': 'string', 'format': 'date'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Equipment change created',
            'examples': {
                'application/json': {'id': 1, 'equipment_id': 5, 'change': 'Replaced battery', 'date': '2025-09-28'}
            }
        }
    }
})
def create_equipmentchange() -> Response:
    content = request.get_json()
    equipmentchange_obj = EquipmentChanges.create_from_dto(content)
    equipment_changes_controller.create(equipmentchange_obj)
    return make_response(jsonify(equipmentchange_obj.put_into_dto()), HTTPStatus.CREATED)


@equipmentchanges_bp.get('/<int:equipmentchange_id>')
@swag_from({
    'tags': ['EquipmentChanges'],
    'summary': 'Get equipment change by ID',
    'parameters': [{'name': 'equipmentchange_id', 'in': 'path', 'type': 'integer', 'required': True}],
    'responses': {
        200: {
            'description': 'Equipment change found',
            'examples': {'application/json': {'id': 1, 'equipment_id': 5, 'change': 'Replaced battery', 'date': '2025-09-28'}}
        },
        404: {'description': 'Equipment change not found'}
    }
})
def get_equipmentchange(equipmentchange_id: int) -> Response:
    return make_response(jsonify(equipment_changes_controller.find_by_id(equipmentchange_id)), HTTPStatus.OK)


@equipmentchanges_bp.put('/<int:equipmentchange_id>')
@swag_from({
    'tags': ['EquipmentChanges'],
    'summary': 'Update equipment change',
    'parameters': [
        {'name': 'equipmentchange_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'EquipmentChange',
                'properties': {
                    'equipment_id': {'type': 'integer'},
                    'change': {'type': 'string'},
                    'date': {'type': 'string', 'format': 'date'}
                }
            }
        }
    ],
    'responses': {200: {'description': 'Equipment change updated'}}
})
def update_equipmentchange(equipmentchange_id: int) -> Response:
    content = request.get_json()
    equipmentchange_obj = EquipmentChanges.create_from_dto(content)
    equipment_changes_controller.update(equipmentchange_id, equipmentchange_obj)
    return make_response("Equipment change updated", HTTPStatus.OK)


@equipmentchanges_bp.patch('/<int:equipmentchange_id>')
@swag_from({
    'tags': ['EquipmentChanges'],
    'summary': 'Patch equipment change',
    'parameters': [
        {'name': 'equipmentchange_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'EquipmentChangePatch',
                'properties': {
                    'equipment_id': {'type': 'integer'},
                    'change': {'type': 'string'},
                    'date': {'type': 'string', 'format': 'date'}
                }
            }
        }
    ],
    'responses': {200: {'description': 'Equipment change patched'}}
})
def patch_equipmentchange(equipmentchange_id: int) -> Response:
    content = request.get_json()
    equipment_changes_controller.patch(equipmentchange_id, content)
    return make_response("Equipment change patched", HTTPStatus.OK)


@equipmentchanges_bp.delete('/<int:equipmentchange_id>')
@swag_from({
    'tags': ['EquipmentChanges'],
    'summary': 'Delete equipment change',
    'parameters': [{'name': 'equipmentchange_id', 'in': 'path', 'type': 'integer', 'required': True}],
    'responses': {200: {'description': 'Equipment change deleted'}}
})
def delete_equipmentchange(equipmentchange_id: int) -> Response:
    equipment_changes_controller.delete(equipmentchange_id)
    return make_response("Equipment change deleted", HTTPStatus.OK)

@equipmentchanges_bp.get('')
def get_all_equipment_changes() -> Response:
    """
    Gets all equipment changes.
    :return: Response object
    """
    changes = equipment_changes_controller.query.all()
    changes_dto = [change.put_into_dto() for change in changes]
    return make_response(jsonify(changes_dto), HTTPStatus.OK)
