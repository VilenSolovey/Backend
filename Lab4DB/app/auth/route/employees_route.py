from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import Employees
from Lab4DB.app.auth.controller import employees_controller
from Lab4DB.app import db
from Lab4DB.app.auth.domain import Requests, RequestsHasEmployees
from Lab4DB.app.auth.domain.employees import insert_employees
employees_bp = Blueprint('employees', __name__, url_prefix='/employees')
from typing import Union
from flask import jsonify, request, make_response
from flask_restx import Namespace
from flasgger import swag_from
api = Namespace('employees', description='Employees related operations')

@employees_bp.get('')
@swag_from({
    'tags': ['Employees'],
    'summary': 'Get all employees',
    'responses': {
        200: {
            'description': 'List of all employees',
            'examples': {
                'application/json': [
                    {'id': 1, 'first_name': 'John', 'last_name': 'Doe'}
                ]
            }
        }
    }
})
def get_all_employees() -> Response:
    return make_response(jsonify(employees_controller.find_all()), HTTPStatus.OK)


@employees_bp.post('')
@swag_from({
    'tags': ['Employees'],
    'summary': 'Create a new employee',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Employee',
                'properties': {
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'position': {'type': 'string'},
                    'email': {'type': 'string'},
                    'phone_number': {'type': 'string'},
                    'middle_name': {'type': 'string'},
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Employee created successfully',
            'examples': {
                'application/json': {
                    'id': 1, 'first_name': 'John', 'last_name': 'Doe'
                }
            }
        },
        400: {'description': 'Invalid input data'},
        500: {'description': 'Internal server error'}
    }
})
def create_employee() -> Response:
    try:
        content = request.get_json()
        if not content:
            return make_response(jsonify({"error": "No input data provided"}), HTTPStatus.BAD_REQUEST)

        employee_obj = Employees.create_from_dto(content)
        if not employee_obj:
            return make_response(jsonify({"error": "Failed to create employee. Invalid data."}), HTTPStatus.BAD_REQUEST)

        employees_controller.create(employee_obj)
        return make_response(jsonify(employee_obj.put_into_dto()), HTTPStatus.CREATED)
    except Exception as e:
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR)


@employees_bp.get('/<int:employee_id>')
@swag_from({
    'tags': ['Employees'],
    'summary': 'Get employee by ID',
    'parameters': [
        {'name': 'employee_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Employee found'},
        404: {'description': 'Employee not found'}
    }
})
def get_employee(employee_id: int) -> Response:
    return make_response(jsonify(employees_controller.find_by_id(employee_id)), HTTPStatus.OK)
@employees_bp.put('/<int:employee_id>')
@swag_from({
    'tags': ['Employees'],
    'summary': 'Update employee by ID',
    'parameters': [
        {'name': 'employee_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Employee',
                'properties': {
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'position': {'type': 'string'},
                    'email': {'type': 'string'},
                    'phone_number': {'type': 'string'},
                    'middle_name': {'type': 'string'},
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Employee updated successfully'},
        400: {'description': 'Invalid input data'},
        500: {'description': 'Internal server error'}
    }
})
def update_employee(employee_id: int) -> Response:
    try:
        content = request.get_json()
        if not content:
            return make_response(jsonify({"error": "No input data provided"}), HTTPStatus.BAD_REQUEST)
        employee_obj = Employees.create_from_dto(content)
        employees_controller.update(employee_id, employee_obj)
        return make_response(jsonify({"message": "Employee updated successfully"}), HTTPStatus.OK)
    except Exception as e:
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR)


@employees_bp.delete('/<int:employee_id>')
@swag_from({
    'tags': ['Employees'],
    'summary': 'Delete employee by ID',
    'parameters': [
        {'name': 'employee_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Employee deleted successfully'},
        404: {'description': 'Employee not found'}
    }
})
def delete_employee(employee_id: int) -> Response:
    employees_controller.delete(employee_id)
    return make_response("Employee deleted", HTTPStatus.OK)


@employees_bp.patch('/<int:employee_id>')
def patch_employee(employee_id: int) -> Response:
    """
    Patches an employee by ID.
    :return: Response object
    """
    content = request.get_json()
    employees_controller.patch(employee_id, content)
    return make_response("Employee updated", HTTPStatus.OK)

@employees_bp.route('/employees/<int:employees_id>/user', methods=['GET'])
def get_users_for_solar_station(employees_id: int) -> Response:
    return make_response(jsonify(employees_controller.find_by_id(employees_id)), HTTPStatus.OK)


@employees_bp.route('/all/requests', methods=['GET'])
def get_all_requests_for_all_employees():
    """
    Виводить всі запити для кожного співробітника.
    """

    results = db.session.query(Employees, Requests). \
        join(RequestsHasEmployees, Employees.id == RequestsHasEmployees.employees_id). \
        join(Requests, Requests.id == RequestsHasEmployees.requests_id). \
        all()

    employees_requests = {}
    for employee, request in results:
        if employee.id not in employees_requests:
            employees_requests[employee.id] = {
                "employee": employee.put_into_dto(),
                "requests": []
            }
        employees_requests[employee.id]["requests"].append(request.put_into_dto())

    return jsonify(employees_requests), 200


@employees_bp.route('/all/employees', methods=['GET'])
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


@employees_bp.route('/auto_insert', methods=['POST'])
def auto_employees_create() -> Union[Response, tuple[Response, int]]:
    num_employees = request.args.get('amount')
    if not num_employees or not num_employees.isdigit():
        return jsonify({"error": "Invalid amount"}), 400

    result = insert_employees(int(num_employees))

    if result != -1:
        res = [employee.put_into_dto() for employee in result]
        return jsonify({"new_employees": res}), HTTPStatus.CREATED
    else:
        return jsonify({"error": "Failed to insert employees"}), 400


