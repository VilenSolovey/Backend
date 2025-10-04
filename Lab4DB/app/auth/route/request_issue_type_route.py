from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import RequestIssueType
from Lab4DB.app.auth.controller import request_issue_type_controller
from flasgger import swag_from

requestissuetype_bp = Blueprint('requestissuetype', __name__, url_prefix='/requestissuetype')


@requestissuetype_bp.get('')
@swag_from({
    'tags': ['RequestIssueType'],
    'summary': 'Get all request issue types',
    'description': 'Returns a list of all request issue types in the database',
    'responses': {
        200: {
            'description': 'A list of request issue types',
            'examples': {
                'application/json': [
                    {'id': 1, 'name': 'Software Issue'},
                    {'id': 2, 'name': 'Hardware Issue'}
                ]
            }
        }
    }
})
def get_all_requestissuetype() -> Response:
    return make_response(jsonify(request_issue_type_controller.find_all()), HTTPStatus.OK)


@requestissuetype_bp.post('')
@swag_from({
    'tags': ['RequestIssueType'],
    'summary': 'Create a new request issue type',
    'description': 'Adds a new request issue type to the table',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'RequestIssueType',
                'properties': {
                    'name': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Request issue type created',
            'examples': {
                'application/json': {'id': 1, 'name': 'Software Issue'}
            }
        }
    }
})
def create_request() -> Response:
    content = request.get_json()
    request_obj = RequestIssueType.create_from_dto(content)
    request_issue_type_controller.create(request_obj)
    return make_response(jsonify(request_obj.put_into_dto()), HTTPStatus.CREATED)


@requestissuetype_bp.get('/<int:request_id>')
@swag_from({
    'tags': ['RequestIssueType'],
    'summary': 'Get request issue type by ID',
    'parameters': [{'name': 'request_id', 'in': 'path', 'type': 'integer', 'required': True}],
    'responses': {
        200: {
            'description': 'Request issue type found',
            'examples': {'application/json': {'id': 1, 'name': 'Software Issue'}}
        },
        404: {'description': 'Request issue type not found'}
    }
})
def get_request(request_id: int) -> Response:
    return make_response(jsonify(request_issue_type_controller.find_by_id(request_id)), HTTPStatus.OK)


@requestissuetype_bp.put('/<int:request_id>')
@swag_from({
    'tags': ['RequestIssueType'],
    'summary': 'Update request issue type',
    'parameters': [
        {'name': 'request_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'RequestIssueType',
                'properties': {'name': {'type': 'string'}}
            }
        }
    ],
    'responses': {200: {'description': 'Request issue type updated'}}
})
def update_request(request_id: int) -> Response:
    content = request.get_json()
    request_obj = RequestIssueType.create_from_dto(content)
    request_issue_type_controller.update(request_id, request_obj)
    return make_response("Request updated", HTTPStatus.OK)


@requestissuetype_bp.patch('/<int:request_id>')
@swag_from({
    'tags': ['RequestIssueType'],
    'summary': 'Patch request issue type',
    'parameters': [
        {'name': 'request_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'RequestIssueTypePatch',
                'properties': {'name': {'type': 'string'}}
            }
        }
    ],
    'responses': {200: {'description': 'Request issue type patched'}}
})
def patch_request(request_id: int) -> Response:
    content = request.get_json()
    request_issue_type_controller.patch(request_id, content)
    return make_response("Request updated", HTTPStatus.OK)


@requestissuetype_bp.delete('/<int:request_id>')
@swag_from({
    'tags': ['RequestIssueType'],
    'summary': 'Delete request issue type',
    'parameters': [{'name': 'request_id', 'in': 'path', 'type': 'integer', 'required': True}],
    'responses': {200: {'description': 'Request issue type deleted'}}
})
def delete_request(request_id: int) -> Response:
    request_issue_type_controller.delete(request_id)
    return make_response("Request deleted", HTTPStatus.OK)

@requestissuetype_bp.get('/<int:issue_type_id>/requests')
def get_requests_for_issue_type(issue_type_id: int):
    """
    Отримує всіх запитів, пов'язаних із конкретним типом проблеми.
    :param issue_type_id: ID типу проблеми
    :return: Об'єкт відповіді
    """
    # Отримуємо тип проблеми за ID
    issue_type = request_issue_type_controller.find_by_id(issue_type_id)

    # Перевіряємо, чи тип проблеми існує
    if issue_type is None:
        return make_response("Тип проблеми не знайдено", HTTPStatus.NOT_FOUND)

    # Отримуємо всі запити, пов'язані з цим типом проблеми
    requests = db.session.query(Requests).\
        join(RequestsHasRequestIssueType, Requests.id == RequestsHasRequestIssueType.requests_id).\
        filter(RequestsHasRequestIssueType.request_issue_type_id == issue_type_id).\
        all()

    # Якщо запити не знайдені, повертаємо 404
    if not requests:
        return make_response("Запити не знайдені", HTTPStatus.NOT_FOUND)

    # Повертаємо запити у вигляді DTO
    requests_dto = [request.put_into_dto() for request in requests]
    return make_response(jsonify(requests_dto), HTTPStatus.OK)
@requestissuetype_bp.route('/all/requests', methods=['GET'])
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
