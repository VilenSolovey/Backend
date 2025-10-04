from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import Software
from Lab4DB.app.auth.controller import software_controller
from flasgger import swag_from

software_bp = Blueprint('software', __name__, url_prefix='/software')


@software_bp.get('')
@swag_from({
    'tags': ['Software'],
    'summary': 'Get all software',
    'description': 'Returns a list of all software entries from the Software table',
    'responses': {
        200: {
            'description': 'List of software entries',
            'examples': {
                'application/json': [
                    {"id": 1, "name": "Windows", "version": "10"},
                    {"id": 2, "name": "Ubuntu", "version": "22.04"}
                ]
            }
        }
    }
})
def get_all_software() -> Response:
    return make_response(jsonify(software_controller.find_all()), HTTPStatus.OK)


@software_bp.post('')
@swag_from({
    'tags': ['Software'],
    'summary': 'Create new software entry',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'id': 'Software',
                'properties': {
                    'name': {'type': 'string'},
                    'version': {'type': 'string'},
                    'license': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Software created'},
        400: {'description': 'Invalid input'}
    }
})
def create_software() -> Response:
    content = request.get_json()
    software_obj = Software.create_from_dto(content)
    software_controller.create(software_obj)
    return make_response(jsonify(software_obj.put_into_dto()), HTTPStatus.CREATED)


@software_bp.get('/<int:software_id>')
@swag_from({
    'tags': ['Software'],
    'summary': 'Get software by ID',
    'parameters': [
        {'name': 'software_id', 'in': 'path', 'required': True, 'type': 'integer'}
    ],
    'responses': {
        200: {'description': 'Software found'},
        404: {'description': 'Software not found'}
    }
})
def get_software(software_id: int) -> Response:
    return make_response(jsonify(software_controller.find_by_id(software_id)), HTTPStatus.OK)


@software_bp.put('/<int:software_id>')
@swag_from({
    'tags': ['Software'],
    'summary': 'Update software',
    'parameters': [
        {'name': 'software_id', 'in': 'path', 'required': True, 'type': 'integer'},
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'type': 'object'}}
    ],
    'responses': {
        200: {'description': 'Software updated'}
    }
})
def update_software(software_id: int) -> Response:
    content = request.get_json()
    software_obj = Software.create_from_dto(content)
    software_controller.update(software_id, software_obj)
    return make_response("Software updated", HTTPStatus.OK)


@software_bp.patch('/<int:software_id>')
@swag_from({
    'tags': ['Software'],
    'summary': 'Patch software',
    'description': 'Updates only specified fields of a software entry',
    'parameters': [
        {'name': 'software_id', 'in': 'path', 'required': True, 'type': 'integer'},
        {'name': 'body', 'in': 'body', 'required': True, 'schema': {'type': 'object'}}
    ],
    'responses': {
        200: {'description': 'Software patched'}
    }
})
def patch_software(software_id: int) -> Response:
    content = request.get_json()
    software_controller.patch(software_id, content)
    return make_response("Software patched", HTTPStatus.OK)


@software_bp.delete('/<int:software_id>')
@swag_from({
    'tags': ['Software'],
    'summary': 'Delete software',
    'parameters': [
        {'name': 'software_id', 'in': 'path', 'required': True, 'type': 'integer'}
    ],
    'responses': {
        200: {'description': 'Software deleted'},
        404: {'description': 'Software not found'}
    }
})
def delete_software(software_id: int) -> Response:
    try:
        software_controller.delete(software_id)
        return make_response(jsonify({"message": "Software deleted successfully"}), HTTPStatus.OK)
    except Exception as e:
        print(f"Error: {e}")
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), HTTPStatus.INTERNAL_SERVER_ERROR)

@software_bp.get('/all/software_issues')
def get_all_issues_for_all_software():
    """
    Gets all software issues for each software in a single request.
    :return: Response object
    """
    all_software = Software.query.all()

    software_issues_data = {}
    for software in all_software:
        issues = SoftwareIssues.query.filter_by(software_id=software.id).all()

        software_issues_data[software.id] = {
            "software": software.put_into_dto(),
            "issues": [issue.put_into_dto() for issue in issues]
        }

    return make_response(jsonify(software_issues_data), HTTPStatus.OK)
@software_bp.route('/create_dynamic_databases', methods=['POST'])
def create_databases_endpoint():
    databases = create_dynamic_databases_from_software()
    if isinstance(databases, str):
        return jsonify({"error": databases}), HTTPStatus.NOT_FOUND
    return jsonify({"message": f"Databases and tables created successfully: {databases}"}), HTTPStatus.CREATED
