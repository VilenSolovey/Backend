from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import Equipment
from Lab4DB.app.auth.controller import equipment_controller

equipment_bp = Blueprint('equipment', __name__, url_prefix='/equipment')


@equipment_bp.get('')
def get_all_equipment() -> Response:
    """
    Gets all equipment from the Equipment table.
    :return: Response object
    """
    return make_response(jsonify(equipment_controller.find_all()), HTTPStatus.OK)


@equipment_bp.post('')
def create_equipment() -> Response:
    """
    Creates a new equipment entry in the Equipment table.
    :return: Response object
    """
    content = request.get_json()
    equipment_obj = Equipment.create_from_dto(content)
    equipment_controller.create(equipment_obj)
    return make_response(jsonify(equipment_obj.put_into_dto()), HTTPStatus.CREATED)


@equipment_bp.get('/<int:equipment_id>')
def get_equipment(equipment_id: int) -> Response:
    """
    Gets an equipment entry by ID.
    :return: Response object
    """
    return make_response(jsonify(equipment_controller.find_by_id(equipment_id)), HTTPStatus.OK)


@equipment_bp.put('/<int:equipment_id>')
def update_equipment(equipment_id: int) -> Response:
    """
    Updates an equipment entry by ID.
    :return: Response object
    """
    content = request.get_json()
    equipment_obj = Equipment.create_from_dto(content)
    equipment_controller.update(equipment_id, equipment_obj)
    return make_response("Equipment updated", HTTPStatus.OK)


@equipment_bp.route('/<int:equipment_id>', methods=['PATCH'])
def patch_equipment(equipment_id: int) -> Response:
    """
    Patches an equipment entry by ID.
    :return: Response object
    """
    content = request.get_json()
    equipment_controller.patch(equipment_id, content)
    return make_response("Equipment patched", HTTPStatus.OK)


@equipment_bp.delete('/<int:equipment_id>')
def delete_equipment(equipment_id: int) -> Response:
    """
    Deletes an equipment entry by ID.
    :return: Response object
    """
    equipment_controller.delete(equipment_id)
    return make_response("Equipment deleted", HTTPStatus.OK)


