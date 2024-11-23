from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import SoftwareIssues
from Lab4DB.app.auth.controller import software_issues_controller

softwareissues_bp = Blueprint('softwareissues', __name__, url_prefix='/softwareissues')


@softwareissues_bp.get('')
def get_all_softwareissues() -> Response:
    """
    Gets all software issues from the SoftwareIssues table.
    :return: Response object
    """
    return make_response(jsonify(software_issues_controller.find_all()), HTTPStatus.OK)


@softwareissues_bp.post('')
def create_softwareissue() -> Response:
    """
    Creates a new software issue in the SoftwareIssues table.
    :return: Response object
    """
    content = request.get_json()
    softwareissue_obj = SoftwareIssues.create_from_dto(content)
    software_issues_controller.create(softwareissue_obj)
    return make_response(jsonify(softwareissue_obj.put_into_dto()), HTTPStatus.CREATED)


@softwareissues_bp.get('/<int:softwareissue_id>')
def get_softwareissue(softwareissue_id: int) -> Response:
    """
    Gets a software issue by ID.
    :return: Response object
    """
    return make_response(jsonify(software_issues_controller.find_by_id(softwareissue_id)), HTTPStatus.OK)


@softwareissues_bp.put('/<int:softwareissue_id>')
def update_softwareissue(softwareissue_id: int) -> Response:
    """
    Updates a software issue by ID.
    :return: Response object
    """
    content = request.get_json()
    softwareissue_obj = SoftwareIssues.create_from_dto(content)
    software_issues_controller.update(softwareissue_id, softwareissue_obj)
    return make_response("Software issue updated", HTTPStatus.OK)


@softwareissues_bp.patch('/<int:softwareissue_id>')
def patch_softwareissue(softwareissue_id: int) -> Response:
    """
    Patches a software issue by ID.
    :return: Response object
    """
    content = request.get_json()
    software_issues_controller.patch(softwareissue_id, content)
    return make_response("Software issue patched", HTTPStatus.OK)


@softwareissues_bp.delete('/<int:softwareissue_id>')
def delete_softwareissue(softwareissue_id: int) -> Response:
    """
    Deletes a software issue by ID.
    :return: Response object
    """
    software_issues_controller.delete(softwareissue_id)
    return make_response("Software issue deleted", HTTPStatus.OK)


