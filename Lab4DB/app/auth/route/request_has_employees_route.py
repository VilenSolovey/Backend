from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import RequestsHasEmployees
from Lab4DB.app.auth.controller import requests_has_employees_controller

requestshasemployees_bp = Blueprint('requestshasemployees', __name__, url_prefix='/requestshasemployees')


@requestshasemployees_bp.get('')
def get_all_requestshasemployees() -> Response:
    """
    Gets all entries from the Requests_has_Employees table.
    :return: Response object
    """
    return make_response(jsonify(requests_has_employees_controller.find_all()), HTTPStatus.OK)


@requestshasemployees_bp.post('')
def create_requesthasemployee() -> Response:
    """
    Creates a new entry in the Requests_has_Employees table.
    :return: Response object
    """
    content = request.get_json()
    requesthasemployee_obj = RequestsHasEmployees.create_from_dto(content)
    requests_has_employees_controller.create(requesthasemployee_obj)
    return make_response(jsonify(requesthasemployee_obj.put_into_dto()), HTTPStatus.CREATED)


@requestshasemployees_bp.get('/<int:requesthasemployee_id>')
def get_requesthasemployee(requesthasemployee_id: int) -> Response:
    """
    Gets an entry by ID.
    :return: Response object
    """
    return make_response(jsonify(requests_has_employees_controller.find_by_id(requesthasemployee_id)), HTTPStatus.OK)


@requestshasemployees_bp.delete('/<int:requesthasemployee_id>')
def delete_requesthasemployee(requesthasemployee_id: int) -> Response:
    """
    Deletes an entry by ID.
    :return: Response object
    """
    requests_has_employees_controller.delete(requesthasemployee_id)
    return make_response("Entry deleted", HTTPStatus.OK)
