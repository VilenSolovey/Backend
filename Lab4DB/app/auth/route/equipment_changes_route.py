from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import equipment_changes
from Lab4DB.app.auth.controller import equipment_changes_controller

equipmentchanges_bp = Blueprint('equipmentchanges', __name__, url_prefix='/equipmentchanges')


@equipmentchanges_bp.get('')
def get_all_equipmentchanges() -> Response:
    """
    Gets all equipment changes from the EquipmentChanges table.
    :return: Response object
    """
    return make_response(jsonify(equipment_changes_controller.find_all()), HTTPStatus.OK)


@equipmentchanges_bp.post('')
def create_equipmentchange() -> Response:
    """
    Creates a new equipment change entry in the EquipmentChanges table.
    :return: Response object
    """
    content = request.get_json()
    equipmentchange_obj = equipment_changes.create_from_dto(content)
    equipment_changes_controller.create(equipmentchange_obj)
    return make_response(jsonify(equipmentchange_obj.put_into_dto()), HTTPStatus.CREATED)


@equipmentchanges_bp.get('/<int:equipmentchange_id>')
def get_equipmentchange(equipmentchange_id: int) -> Response:
    """
    Gets an equipment change entry by ID.
    :return: Response object
    """
    return make_response(jsonify(equipment_changes_controller.find_by_id(equipmentchange_id)), HTTPStatus.OK)


@equipmentchanges_bp.put('/<int:equipmentchange_id>')
def update_equipmentchange(equipmentchange_id: int) -> Response:
    """
    Updates an equipment change entry by ID.
    :return: Response object
    """
    content = request.get_json()
    equipmentchange_obj = equipment_changes.create_from_dto(content)
    equipment_changes_controller.update(equipmentchange_id, equipmentchange_obj)
    return make_response("Equipment change updated", HTTPStatus.OK)

@equipmentchanges_bp.patch('/<int:equipmentchange_id>')
def patch_equipmentchange(equipmentchange_id: int) -> Response:
    """
    Patches an equipment change entry by ID.
    :return: Response object
    """
    content = request.get_json()

    equipment_changes_controller.patch(equipmentchange_id, content)
    return make_response("Equipment change patched", HTTPStatus.OK)


@equipmentchanges_bp.delete('/<int:equipmentchange_id>')
def delete_equipmentchange(equipmentchange_id: int) -> Response:
    """
    Deletes an equipment change entry by ID.
    :return: Response object
    """
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