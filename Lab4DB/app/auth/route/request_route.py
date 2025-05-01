from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import Requests, Employees, RequestsHasEmployees, RequestIssueType, RequestsHasRequestIssueType
from Lab4DB.app.auth.controller import requests_controller
from Lab4DB.app.auth.domain import SoftwareUpdates, Software
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


@requests_bp.get('/all/software_updates')
def get_all_software_updates_for_all_requests():
    """
    Gets all software updates for each request in a single request.
    :return: Response object
    """
    all_requests = Requests.query.all()

    requests_software_updates_data = {}
    for request in all_requests:
        software_updates = SoftwareUpdates.query.filter_by(requests_id=request.id).all()

        requests_software_updates_data[request.id] = {
            "request": request.put_into_dto(),
            "software_updates": [update.put_into_dto() for update in software_updates]
        }

    return make_response(jsonify(requests_software_updates_data), HTTPStatus.OK)


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


@requests_bp.route('/all/issue_types', methods=['GET'])
def get_all_issue_types_for_all_requests():
    """
    Виводить всі типи проблем для кожного запиту.
    """
    results = db.session.query(Requests, RequestIssueType).\
        join(RequestsHasRequestIssueType, Requests.id == RequestsHasRequestIssueType.requests_id).\
        join(RequestIssueType, RequestIssueType.id == RequestsHasRequestIssueType.request_issue_type_id).\
        all()

    requests_issue_types = {}
    for request, issue_type in results:
        if request.id not in requests_issue_types:
            requests_issue_types[request.id] = {
                "request": request.put_into_dto(),
                "issue_types": []
            }
        requests_issue_types[request.id]["issue_types"].append(issue_type.put_into_dto())

    return jsonify(requests_issue_types), 200

@requests_bp.route('/all/requests', methods=['GET'])
def get_all_requests_for_all_issue_types():
    """
    Виводить всі запити для кожного типу проблем.
    """
    results = db.session.query(RequestIssueType, Requests).\
        join(RequestsHasRequestIssueType, RequestIssueType.id == RequestsHasRequestIssueType.request_issue_type_id).\
        join(Requests, Requests.id == RequestsHasRequestIssueType.requests_id).\
        all()

    issue_types_requests = {}
    for issue_type, request in results:
        if issue_type.id not in issue_types_requests:
            issue_types_requests[issue_type.id] = {
                "issue_type": issue_type.put_into_dto(),
                "requests": []
            }
        issue_types_requests[issue_type.id]["requests"].append(request.put_into_dto())

    return jsonify(issue_types_requests), 200


@requests_bp.route('/all/employees', methods=['GET'])
def get_all_employees_for_all_requests():
    """
    Виводить всіх співробітників для кожного запиту.
    """

    results = db.session.query(Requests, Employees). \
        join(RequestsHasEmployees, Requests.id == RequestsHasEmployees.requests_id). \
        join(Employees, Employees.id == RequestsHasEmployees.employees_id). \
        all()

    requests_employees = {}
    for request, employee in results:
        if request.id not in requests_employees:
            requests_employees[request.id] = {
                "request": request.put_into_dto(),
                "employees": []
            }
        requests_employees[request.id]["employees"].append(employee.put_into_dto())

    return jsonify(requests_employees), 200
