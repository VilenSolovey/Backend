from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import RequestPriority
from Lab4DB.app.auth.controller import request_priority_controller

requestpriority_bp = Blueprint('requestpriority', __name__, url_prefix='/requestpriority')

@requestpriority_bp.get('')
def get_all_requestpriority() -> Response:
    return make_response(jsonify(request_priority_controller.find_all()), HTTPStatus.OK)

@requestpriority_bp.post('')
def create_request() -> Response:
    """
    Creates a new request in the Requests table.
    :return: Response object
    """
    content = request.get_json()
    request_obj = RequestPriority.create_from_dto(content)
    request_priority_controller.create(request_obj)
    return make_response(jsonify(request_obj.put_into_dto()), HTTPStatus.CREATED)


@requestpriority_bp.get('/<int:request_priority_id>')
def get_request(request_priority_id: int) -> Response:
    """
    Gets a request by ID.
    :return: Response object
    """
    return make_response(jsonify(request_priority_controller.find_by_id(request_priority_id)), HTTPStatus.OK)


@requestpriority_bp.put('/<int:request_priority_id>')
def update_request(request_priority_id: int) -> Response:
    """
    Updates a request by ID.
    :return: Response object
    """
    content = request.get_json()
    request_obj = RequestPriority.create_from_dto(content)
    request_priority_controller.update(request_priority_id, request_obj)
    return make_response("Request updated", HTTPStatus.OK)


@requestpriority_bp.patch('/<int:request_priority_id>')
def patch_request(request_priority_id: int) -> Response:
    """
    Patches a request by ID.
    :return: Response object
    """
    content = request.get_json()
    request_priority_controller.patch(request_priority_id, content)
    return make_response("Request updated", HTTPStatus.OK)


@requestpriority_bp.delete('/<int:request_priority_id>')
def delete_request(request_priority_id: int) -> Response:
    """
    Deletes a request by ID.
    :return: Response object
    """
    request_priority_controller.delete(request_priority_id)
    return make_response("Request deleted", HTTPStatus.OK)

