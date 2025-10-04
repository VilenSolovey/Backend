from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import Requests
from Lab4DB.app.auth.controller import requests_controller
from flasgger import swag_from

requests_bp = Blueprint('requests', __name__, url_prefix='/requests')


@requests_bp.get('')
@swag_from({
    'tags': ['Requests'],
    'summary': 'Get all requests',
    'description': 'Returns a list of all requests in the database',
    'responses': {
        200: {
            'description': 'List of requests',
            'examples': {
                'application/json': [
                    {"id": 1, "description": "Network issue", "status": "Pending"},
                    {"id": 2, "description": "Printer not working", "status": "Resolved"}
                ]
            }
        }
    }
})
def get_all_requests() -> Response:
    return make_response(jsonify(requests_controller.find_all()), HTTPStatus.OK)


@requests_bp.post('')
@swag_from({
    'tags': ['Requests'],
    'summary': 'Create a new request',
    'description': 'Creates a new request entry in the Requests table',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Request',
                'properties': {
                    'description': {'type': 'string'},
                    'creation_time': {'type': 'string', 'format': 'date-time'},
                    'requeststatusid': {'type': 'integer'},
                    'requestpriority_id': {'type': 'integer'},
                    'locations_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Request created',
            'examples': {
                'application/json': {"id": 1, "description": "New request created"}
            }
        }
    }
})
def create_request() -> Response:
    content = request.get_json()
    request_obj = Requests.create_from_dto(content)
    requests_controller.create(request_obj)
    return make_response(jsonify(request_obj.put_into_dto()), HTTPStatus.CREATED)


@requests_bp.get('/<int:request_id>')
@swag_from({
    'tags': ['Requests'],
    'summary': 'Get request by ID',
    'parameters': [
        {'name': 'request_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {
            'description': 'Request found',
            'examples': {
                'application/json': {"id": 1, "description": "Network issue", "status": "Pending"}
            }
        },
        404: {'description': 'Request not found'}
    }
})
def get_request(request_id: int) -> Response:
    return make_response(jsonify(requests_controller.find_by_id(request_id)), HTTPStatus.OK)


@requests_bp.put('/<int:request_id>')
@swag_from({
    'tags': ['Requests'],
    'summary': 'Update a request',
    'description': 'Updates a request entry by ID',
    'parameters': [
        {'name': 'request_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'description': {'type': 'string'},
                    'requeststatusid': {'type': 'integer'},
                    'requestpriority_id': {'type': 'integer'},
                    'locations_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Request updated'}
    }
})
def update_request(request_id: int) -> Response:
    content = request.get_json()
    request_obj = Requests.create_from_dto(content)
    requests_controller.update(request_id, request_obj)
    return make_response("Request updated", HTTPStatus.OK)


@requests_bp.patch('/<int:request_id>')
@swag_from({
    'tags': ['Requests'],
    'summary': 'Patch request',
    'description': 'Updates only provided fields of a request',
    'parameters': [
        {'name': 'request_id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'body', 'in': 'body', 'schema': {'type': 'object'}}
    ],
    'responses': {
        200: {'description': 'Request patched'}
    }
})
def patch_request(request_id: int) -> Response:
    content = request.get_json()
    requests_controller.patch(request_id, content)
    return make_response("Request updated", HTTPStatus.OK)


@requests_bp.delete('/<int:request_id>')
@swag_from({
    'tags': ['Requests'],
    'summary': 'Delete a request',
    'description': 'Deletes a request entry by ID',
    'parameters': [
        {'name': 'request_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Request deleted'},
        404: {'description': 'Request not found'}
    }
})
def delete_request(request_id: int) -> Response:
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
