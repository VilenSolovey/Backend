from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain.tasks import Tasks
from Lab4DB.app.auth.controller import tasks_controller
from Lab4DB.app.auth.domain import Employees
task_bp = Blueprint('task', __name__, url_prefix='/tasks')


@task_bp.get('')
def get_all_tasks() -> Response:
    """
    Gets all tasks entries from the Tasks table.
    :return: Response object
    """
    return make_response(jsonify(tasks_controller.find_all()), HTTPStatus.OK)


@task_bp.post('')
def create_task() -> Response:
    """
    Creates a new task entry in the Tasks table.
    :return: Response object
    """
    content = request.get_json()
    try:
        task_obj = Tasks.create_from_dto(content)
        tasks_controller.create(task_obj)
        return make_response(jsonify(task_obj.put_into_dto()), HTTPStatus.CREATED)
    except ValueError as e:
        return make_response(jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST)


@task_bp.get('/<int:task_id>')
def get_task(task_id: int) -> Response:
    """
    Gets a task entry by ID.
    :return: Response object
    """
    return make_response(jsonify(tasks_controller.find_by_id(task_id)), HTTPStatus.OK)


@task_bp.put('/<int:task_id>')
def update_task(task_id: int) -> Response:
    """
    Updates a task entry by ID.
    :return: Response object
    """
    content = request.get_json()
    task_obj = Tasks.create_from_dto(content)
    tasks_controller.update(task_id, task_obj)
    return make_response("Task updated", HTTPStatus.OK)


@task_bp.patch('/<int:task_id>')
def patch_task(task_id: int) -> Response:
    """
    Patches a task entry by ID.
    :return: Response object
    """
    content = request.get_json()
    tasks_controller.patch(task_id, content)
    return make_response("Task patched", HTTPStatus.OK)


@task_bp.delete('/<int:task_id>')
def delete_task(task_id: int) -> Response:
    """
    Deletes a task entry by ID.
    :return: Response object
    """
    tasks_controller.delete(task_id)
    return make_response("Task deleted", HTTPStatus.OK)


@task_bp.get('/<int:task_id>/employee')
def get_task_employee(task_id: int) -> Response:
    """
    Gets the employee assigned to a task.
    :return: Response object
    """
    task = Tasks.query.get(task_id)
    if not task:
        return make_response("Task not found", HTTPStatus.NOT_FOUND)

    employee = task.employee_id
    if not employee:
        return make_response("Employee not found", HTTPStatus.NOT_FOUND)

    employee_obj = Employees.query.get(employee)
    if not employee_obj:
        return make_response("Employee not found", HTTPStatus.NOT_FOUND)

    return make_response(jsonify(employee_obj.put_into_dto()), HTTPStatus.OK)


@task_bp.get('/all/tasks_employees')
def get_all_tasks_with_employees():
    """
    Gets all tasks with assigned employees in a single request.
    :return: Response object
    """
    all_tasks = Tasks.query.all()

    tasks_employees_data = {}
    for task in all_tasks:
        employee_id = task.employee_id
        employee = Employees.query.get(employee_id) if employee_id else None

        tasks_employees_data[task.id] = {
            "task": task.put_into_dto(),
            "employee": employee.put_into_dto() if employee else None
        }

    return make_response(jsonify(tasks_employees_data), HTTPStatus.OK)