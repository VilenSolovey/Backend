from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import RequestStatus
from Lab4DB.app.auth.controller import request_status_controller

requeststatus_bp = Blueprint('requeststatus', __name__, url_prefix='/requeststatus')


@requeststatus_bp.get('')
def get_all_requeststatus() -> Response:
    """
    Gets all request statuses from the RequestStatus table.
    :return: Response object
    """
    return make_response(jsonify(request_status_controller.find_all()), HTTPStatus.OK)


@requeststatus_bp.post('')
def create_requeststatus() -> Response:
    """
    Creates a new request status in the RequestStatus table.
    :return: Response object
    """
    content = request.get_json()
    requeststatus_obj = RequestStatus.create_from_dto(content)
    request_status_controller.create(requeststatus_obj)
    return make_response(jsonify(requeststatus_obj.put_into_dto()), HTTPStatus.CREATED)

@requeststatus_bp.put('/<int:requeststatus_id>')
def update_requeststatus(requeststatus_id: int) -> Response:
    """
    Updates a request status by ID.
    :return: Response object
    """
    content = request.get_json()
    requeststatus_obj = RequestStatus.create_from_dto(content)
    request_status_controller.update(requeststatus_id, requeststatus_obj)
    return make_response("Request status updated", HTTPStatus.OK)


@requeststatus_bp.patch('/<int:requeststatus_id>')
def patch_requeststatus(requeststatus_id: int) -> Response:
    """
    Patches a request status by ID.
    :return: Response object
    """
    content = request.get_json()
    request_status_controller.patch(requeststatus_id, content)
    return make_response("Request status patched", HTTPStatus.OK)


@requeststatus_bp.delete('/<int:requeststatus_id>')
def delete_requeststatus(requeststatus_id: int) -> Response:
    """
    Deletes a request status by ID.
    :return: Response object
    """
    request_status_controller.delete(requeststatus_id)
    return make_response("Request status deleted", HTTPStatus.OK)
