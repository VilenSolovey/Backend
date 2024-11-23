from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import Software
from Lab4DB.app.auth.controller import software_controller
from Lab4DB.app.auth.domain.software_issues import SoftwareIssues
software_bp = Blueprint('software', __name__, url_prefix='/software')


@software_bp.get('')
def get_all_software() -> Response:
    """
    Gets all software entries from the Software table.
    :return: Response object
    """
    return make_response(jsonify(software_controller.find_all()), HTTPStatus.OK)


@software_bp.post('')
def create_software() -> Response:
    """
    Creates a new software entry in the Software table.
    :return: Response object
    """
    content = request.get_json()
    software_obj = Software.create_from_dto(content)
    software_controller.create(software_obj)
    return make_response(jsonify(software_obj.put_into_dto()), HTTPStatus.CREATED)


@software_bp.get('/<int:software_id>')
def get_software(software_id: int) -> Response:
    """
    Gets a software entry by ID.
    :return: Response object
    """
    return make_response(jsonify(software_controller.find_by_id(software_id)), HTTPStatus.OK)


@software_bp.put('/<int:software_id>')
def update_software(software_id: int) -> Response:
    """
    Updates a software entry by ID.
    :return: Response object
    """
    content = request.get_json()
    software_obj = Software.create_from_dto(content)
    software_controller.update(software_id, software_obj)
    return make_response("Software updated", HTTPStatus.OK)


@software_bp.patch('/<int:software_id>')
def patch_software(software_id: int) -> Response:
    """
    Patches a software entry by ID.
    :return: Response object
    """
    content = request.get_json()
    software_controller.patch(software_id, content)
    return make_response("Software patched", HTTPStatus.OK)


@software_bp.delete('/<int:software_id>')
def delete_software(software_id: int) -> Response:
    """
    Deletes a software entry by ID.
    :return: Response object
    """
    software_controller.delete(software_id)
    return make_response("Software deleted", HTTPStatus.OK)

@software_bp.get('/<int:software_id>/software_issues')
def get_issues_for_software(software_id: int) -> Response:
    """
    Gets all software issues for a specific software.
    :param software_id: ID of the software
    :return: Response object
    """

    software_dto = software_controller.find_by_id(software_id)

    if not software_dto:
        return make_response("Software not found", HTTPStatus.NOT_FOUND)

    software_issues = SoftwareIssues.query.filter_by(software_id=software_id).all()

    sofware_issues_dto = [issue.put_into_dto() for issue in software_issues]

    return make_response(jsonify(sofware_issues_dto), HTTPStatus.OK)