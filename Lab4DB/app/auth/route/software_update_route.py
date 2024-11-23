from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import SoftwareUpdates
from Lab4DB.app.auth.controller import software_updates_controller

softwareupdates_bp = Blueprint('softwareupdates', __name__, url_prefix='/softwareupdates')


@softwareupdates_bp.get('')
def get_all_softwareupdates() -> Response:
    """
    Gets all software updates from the SoftwareUpdates table.
    :return: Response object
    """
    return make_response(jsonify(software_updates_controller.find_all()), HTTPStatus.OK)


@softwareupdates_bp.post('')
def create_softwareupdate() -> Response:
    """
    Creates a new software update in the SoftwareUpdates table.
    :return: Response object
    """
    content = request.get_json()
    softwareupdate_obj = SoftwareUpdates.create_from_dto(content)
    software_updates_controller.create(softwareupdate_obj)
    return make_response(jsonify(softwareupdate_obj.put_into_dto()), HTTPStatus.CREATED)


@softwareupdates_bp.get('/<int:softwareupdate_id>')
def get_softwareupdate(softwareupdate_id: int) -> Response:
    """
    Gets a software update by ID.
    :return: Response object
    """
    return make_response(jsonify(software_updates_controller.find_by_id(softwareupdate_id)), HTTPStatus.OK)


@softwareupdates_bp.put('/<int:softwareupdate_id>')
def update_softwareupdate(softwareupdate_id: int) -> Response:
    """
    Updates a software update by ID.
    :return: Response object
    """
    content = request.get_json()
    softwareupdate_obj = SoftwareUpdates.create_from_dto(content)
    software_updates_controller.update(softwareupdate_id, softwareupdate_obj)
    return make_response("Software update updated", HTTPStatus.OK)


@softwareupdates_bp.patch('/<int:softwareupdate_id>')
def patch_softwareupdate(softwareupdate_id: int) -> Response:
    """
    Patches a software update by ID.
    :return: Response object
    """
    content = request.get_json()
    software_updates_controller.patch(softwareupdate_id, content)
    return make_response("Software update patched", HTTPStatus.OK)


@softwareupdates_bp.delete('/<int:softwareupdate_id>')
def delete_softwareupdate(softwareupdate_id: int) -> Response:
    """
    Deletes a software update by ID.
    :return: Response object
    """
    software_updates_controller.delete(softwareupdate_id)
    return make_response("Software update deleted", HTTPStatus.OK)
