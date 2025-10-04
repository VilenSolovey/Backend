from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import RequestsHasEmployees
from Lab4DB.app.auth.controller import requests_has_employees_controller
from flasgger import swag_from

requestshasemployees_bp = Blueprint('requestshasemployees', __name__, url_prefix='/requestshasemployees')


@requestshasemployees_bp.get('')
@swag_from({
    'tags': ['Requests_has_Employees'],
    'summary': 'Get all request-employee relations',
    'description': 'Returns all entries from the Requests_has_Employees table',
    'responses': {
        200: {
            'description': 'List of relations',
            'examples': {
                'application/json': [
                    {"requests_id": 1, "employees_id": 2},
                    {"requests_id": 2, "employees_id": 3}
                ]
            }
        }
    }
})
def get_all_requestshasemployees() -> Response:
    return make_response(jsonify(requests_has_employees_controller.find_all()), HTTPStatus.OK)


@requestshasemployees_bp.post('')
@swag_from({
    'tags': ['Requests_has_Employees'],
    'summary': 'Create a new relation',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'properties': {
                    'requests_id': {'type': 'integer'},
                    'employees_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Relation created',
            'examples': {
                'application/json': {"requests_id": 1, "employees_id": 2}
            }
        }
    }
})
def create_requesthasemployee() -> Response:
    content = request.get_json()
    requesthasemployee_obj = RequestsHasEmployees.create_from_dto(content)
    requests_has_employees_controller.create(requesthasemployee_obj)
    return make_response(jsonify(requesthasemployee_obj.put_into_dto()), HTTPStatus.CREATED)


@requestshasemployees_bp.get('/<int:requesthasemployee_id>')
@swag_from({
    'tags': ['Requests_has_Employees'],
    'summary': 'Get relation by ID',
    'parameters': [
        {'name': 'requesthasemployee_id', 'in': 'path', 'required': True, 'type': 'integer'}
    ],
    'responses': {
        200: {'description': 'Relation found'},
        404: {'description': 'Relation not found'}
    }
})
def get_requesthasemployee(requesthasemployee_id: int) -> Response:
    return make_response(jsonify(requests_has_employees_controller.find_by_id(requesthasemployee_id)), HTTPStatus.OK)


@requestshasemployees_bp.delete('/<int:requests_id>/<int:employees_id>')
@swag_from({
    'tags': ['Requests_has_Employees'],
    'summary': 'Delete relation',
    'parameters': [
        {'name': 'requests_id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'employees_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Relation deleted'},
        404: {'description': 'Relation not found'}
    }
})
def delete_requesthasemployee(requests_id: int, employees_id: int) -> Response:
    requesthasemployee_obj = requests_has_employees_controller.find_by_ids(requests_id, employees_id)
    if not requesthasemployee_obj:
        return make_response("Entry not found", HTTPStatus.NOT_FOUND)

    requests_has_employees_controller.delete(requests_id, employees_id)
    return make_response("Entry deleted", HTTPStatus.OK)


@requestshasemployees_bp.patch('/<int:requests_id>/<int:employees_id>')
@swag_from({
    'tags': ['Requests_has_Employees'],
    'summary': 'Patch relation',
    'description': 'Update only some fields in Requests_has_Employees',
    'parameters': [
        {'name': 'requests_id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'employees_id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'body', 'in': 'body', 'schema': {'type': 'object'}}
    ],
    'responses': {
        200: {'description': 'Relation patched'},
        404: {'description': 'Relation not found'}
    }
})
def patch_requesthasemployee(requests_id: int, employees_id: int) -> Response:
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
@swag_from({
    'tags': ['Requests_has_Employees'],
    'summary': 'Update relation',
    'description': 'Replace an entry in Requests_has_Employees',
    'parameters': [
        {'name': 'requests_id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'employees_id', 'in': 'path', 'type': 'integer', 'required': True},
        {'name': 'body', 'in': 'body', 'schema': {'type': 'object'}}
    ],
    'responses': {
        200: {'description': 'Relation updated'}
    }
})
def update_requesthasemployee(requests_id: int, employees_id: int) -> Response:
    content = request.get_json()
    new_obj = RequestsHasEmployees.create_from_dto(content)
    new_obj.requests_id = requests_id
    new_obj.employees_id = employees_id

    requests_has_employees_controller.update(requests_id, employees_id, new_obj)
    return make_response(jsonify(new_obj.put_into_dto()), HTTPStatus.OK)


@requestshasemployees_bp.route('/new_link', methods=['POST'])
def add_employee_to_request():
    data = request.get_json()
    description = data['description']
    first_name = data['first_name']
    last_name = data['last_name']

    try:
        new_link = RequestsHasEmployees.add_request_to_employee(description, first_name, last_name)
        return make_response(jsonify(new_link.put_into_dto()), HTTPStatus.CREATED)
    except ValueError as e:
        return make_response(str(e), HTTPStatus.BAD_REQUEST)

