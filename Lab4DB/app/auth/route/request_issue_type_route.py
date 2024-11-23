from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import RequestIssueType, RequestsHasRequestIssueType, Requests
from Lab4DB.app.auth.controller import request_issue_type_controller
from Lab4DB.app import db

requestissuetype_bp = Blueprint('requestissuetype', __name__, url_prefix='/requestissuetype')


@requestissuetype_bp.get('')
def get_all_requestissuetype() -> Response:
    return make_response(jsonify(request_issue_type_controller.find_all()), HTTPStatus.OK)

@requestissuetype_bp.post('')
def create_request() -> Response:
    """
    Creates a new request in the Requests table.
    :return: Response object
    """
    content = request.get_json()
    request_obj = RequestIssueType.create_from_dto(content)
    request_issue_type_controller.create(request_obj)
    return make_response(jsonify(request_obj.put_into_dto()), HTTPStatus.CREATED)


@requestissuetype_bp.get('/<int:request_id>')
def get_request(request_id: int) -> Response:
    """
    Gets a request by ID.
    :return: Response object
    """
    return make_response(jsonify(request_issue_type_controller.find_by_id(request_id)), HTTPStatus.OK)


@requestissuetype_bp.put('/<int:request_id>')
def update_request(request_id: int) -> Response:
    """
    Updates a request by ID.
    :return: Response object
    """
    content = request.get_json()
    request_obj = RequestIssueType.create_from_dto(content)
    request_issue_type_controller.update(request_id, request_obj)
    return make_response("Request updated", HTTPStatus.OK)


@requestissuetype_bp.patch('/<int:request_id>')
def patch_request(request_id: int) -> Response:
    """
    Patches a request by ID.
    :return: Response object
    """
    content = request.get_json()
    request_issue_type_controller.patch(request_id, content)
    return make_response("Request updated", HTTPStatus.OK)


@requestissuetype_bp.delete('/<int:request_id>')
def delete_request(request_id: int) -> Response:
    """
    Deletes a request by ID.
    :return: Response object
    """
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
