from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import Requests, Employees, RequestsHasEmployees, RequestIssueType, RequestsHasRequestIssueType
from Lab4DB.app.auth.controller import requests_controller
from Lab4DB.app.auth.domain import SoftwareUpdates
from Lab4DB.app import db

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')


@requests_bp.get('')
def get_all_requests() -> Response:
    """
    Gets all requests from the Requests table.
    :return: Response object
    """
    return make_response(jsonify(requests_controller.find_all()), HTTPStatus.OK)


@requests_bp.post('')
def create_request() -> Response:
    """
    Creates a new request in the Requests table.
    :return: Response object
    """
    content = request.get_json()
    request_obj = Requests.create_from_dto(content)
    requests_controller.create(request_obj)
    return make_response(jsonify(request_obj.put_into_dto()), HTTPStatus.CREATED)


@requests_bp.get('/<int:request_id>')
def get_request(request_id: int) -> Response:
    """
    Gets a request by ID.
    :return: Response object
    """
    return make_response(jsonify(requests_controller.find_by_id(request_id)), HTTPStatus.OK)


@requests_bp.put('/<int:request_id>')
def update_request(request_id: int) -> Response:
    """
    Updates a request by ID.
    :return: Response object
    """
    content = request.get_json()
    request_obj = Requests.create_from_dto(content)
    requests_controller.update(request_id, request_obj)
    return make_response("Request updated", HTTPStatus.OK)


@requests_bp.patch('/<int:request_id>')
def patch_request(request_id: int) -> Response:
    """
    Patches a request by ID.
    :return: Response object
    """
    content = request.get_json()
    requests_controller.patch(request_id, content)
    return make_response("Request updated", HTTPStatus.OK)


@requests_bp.delete('/<int:request_id>')
def delete_request(request_id: int) -> Response:
    """
    Deletes a request by ID.
    :return: Response object
    """
    requests_controller.delete(request_id)
    return make_response("Request deleted", HTTPStatus.OK)


@requests_bp.get('/<int:request_id>/software_updates')
def get_software_updates_for_request(request_id: int):
    """
    Gets all software updates for a specific request.
    :param request_id: ID of the request
    :return: Response object
    """
    request_dto = requests_controller.find_by_id(request_id)

    if not request_dto:
        return make_response("Request not found", HTTPStatus.NOT_FOUND)
    software_updates = SoftwareUpdates.query.filter_by(requests_id=request_dto['id']).all()

    software_updates_dto = [update.put_into_dto() for update in software_updates]

    return make_response(jsonify(software_updates_dto), HTTPStatus.OK)

@requests_bp.get('/<int:request_id>/employees')
def get_employees_for_request(request_id: int):
    """
    Отримує всіх співробітників, пов'язаних із конкретним запитом.
    :param request_id: ID запиту
    :return: Об'єкт відповіді
    """
    request = requests_controller.find_by_id(request_id)

    if request is None:
        return make_response("Запит не знайдено", HTTPStatus.NOT_FOUND)

    employees = db.session.query(Employees).\
        join(RequestsHasEmployees, Employees.id == RequestsHasEmployees.employees_id).\
        filter(RequestsHasEmployees.requests_id == request_id).\
        all()

    if not employees:
        return make_response("Співробітники не знайдені", HTTPStatus.NOT_FOUND)

    employees_dto = [employee.put_into_dto() for employee in employees]
    return make_response(jsonify(employees_dto), HTTPStatus.OK)


@requests_bp.get('/<int:request_id>/issue_types')
def get_issue_types_for_request(request_id: int):
    """
    Отримує всіх типів проблем, пов'язаних із конкретним запитом.
    :param request_id: ID запиту
    :return: Об'єкт відповіді
    """
    request = requests_controller.find_by_id(request_id)

    if request is None:
        return make_response("Запит не знайдено", HTTPStatus.NOT_FOUND)

    issue_types = db.session.query(RequestIssueType).\
        join(RequestsHasRequestIssueType, RequestIssueType.id == RequestsHasRequestIssueType.request_issue_type_id).\
        filter(RequestsHasRequestIssueType.requests_id == request_id).\
        all()

    if not issue_types:
        return make_response("Типи проблем не знайдені", HTTPStatus.NOT_FOUND)

    issue_types_dto = [issue_type.put_into_dto() for issue_type in issue_types]
    return make_response(jsonify(issue_types_dto), HTTPStatus.OK)
