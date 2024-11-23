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


@requestshasemployees_bp.delete('/<int:requests_id>/<int:employees_id>')
def delete_requesthasemployee(requests_id: int, employees_id: int) -> Response:
    """
    Видаляє запис з таблиці Requests_has_Employees за ідентифікаторами requests_id та employees_id.
    :return: Об'єкт відповіді
    """
    requesthasemployee_obj = requests_has_employees_controller.find_by_ids(requests_id, employees_id)
    if not requesthasemployee_obj:
        return make_response("Entry not found", HTTPStatus.NOT_FOUND)


    requests_has_employees_controller.delete(requests_id, employees_id)
    return make_response("Entry deleted", HTTPStatus.OK)

@requestshasemployees_bp.patch('/<int:requests_id>/<int:employees_id>')
def patch_requesthasemployee(requests_id: int, employees_id: int) -> Response:
    """
    Updates a specific entry in the Requests_has_Employees table.
    :return: Response object
    """
    content = request.get_json()

    requesthasemployee_obj = requests_has_employees_controller.find_by_ids(requests_id, employees_id)
    if not requesthasemployee_obj:
        return make_response("Entry not found", HTTPStatus.NOT_FOUND)

    if "requests_id" in content:
        requesthasemployee_obj.requests_id = content["requests_id"]
    if "employees_id" in content:
        requesthasemployee_obj.employees_id = content["employees_id"]

    requests_has_employees_controller.update(requesthasemployee_obj, requesthasemployee_obj)

    return make_response(jsonify(requesthasemployee_obj.put_into_dto()), HTTPStatus.OK)


@requestshasemployees_bp.put('/<int:requests_id>/<int:employees_id>')
def update_requesthasemployee(requests_id: int, employees_id: int) -> Response:
    """
    Оновлює запис в таблиці Requests_has_Employees.
    :return: Об'єкт відповіді
    """
    content = request.get_json()

    new_obj = RequestsHasEmployees.create_from_dto(content)
    new_obj.requests_id = requests_id
    new_obj.employees_id = employees_id

    requests_has_employees_controller.update(requests_id, employees_id, new_obj)

    return make_response(jsonify(new_obj.put_into_dto()), HTTPStatus.OK)

