from http import HTTPStatus
from flask import Blueprint, jsonify, Response, request, make_response
from Lab4DB.app.auth.domain import Locations, Software
from Lab4DB.app.auth.controller import locations_controller
from Lab4DB.app import db
from Lab4DB.app.auth.domain.locations import get_location_stat
locations_bp = Blueprint('locations', __name__, url_prefix='/locations')


@locations_bp.get('')
def get_all_locations() -> Response:
    """Gets all locations from the Locations table."""
    return make_response(jsonify(locations_controller.find_all()), HTTPStatus.OK)


@locations_bp.post('')
def create_location() -> Response:
    """Creates a new location in the Locations table."""
    content = request.get_json()
    location_obj = Locations.create_from_dto(content)
    locations_controller.create(location_obj)
    return make_response(jsonify(location_obj.put_into_dto()), HTTPStatus.CREATED)


@locations_bp.get('/<int:location_id>')
def get_location(location_id: int) -> Response:
    """Gets a location by ID."""
    return make_response(jsonify(locations_controller.find_by_id(location_id)), HTTPStatus.OK)


@locations_bp.put('/<int:location_id>')
def update_location(location_id: int) -> Response:
    """Updates a location by ID."""
    content = request.get_json()
    location_obj = Locations.create_from_dto(content)
    locations_controller.update(location_id, location_obj)
    return make_response("Location updated", HTTPStatus.OK)


@locations_bp.patch('/<int:location_id>')
def patch_location(location_id: int) -> Response:
    """Patches a location by ID."""
    content = request.get_json()
    locations_controller.patch(location_id, content)
    return make_response("Location patched", HTTPStatus.OK)


@locations_bp.delete('/<int:location_id>')
def delete_location(location_id: int) -> Response:
    """Deletes a location by ID."""
    locations_controller.delete(location_id)
    return make_response("Location deleted", HTTPStatus.OK)


@locations_bp.get('/<int:location_id>/requests')
def get_requests_for_location(location_id: int) -> Response:
    """Gets all requests for a specific location."""
    location = db.session.query(Locations).get(location_id)
    if location is None:
        return make_response("Location not found!!", HTTPStatus.NOT_FOUND)
    requests = location.requests
    if not requests:
        return make_response("No requests!", HTTPStatus.NOT_FOUND)
    requests_dto = [request.put_into_dto() for request in requests]
    return make_response(jsonify(requests_dto), HTTPStatus.OK)


@locations_bp.get('/all/software')
def get_all_software_for_all_locations():
    """
    Gets all software for each location.
    :return: Response object
    """
    results = db.session.query(Locations, Software).\
        join(Software, Locations.id == Software.locations_id).\
        all()

    locations_software = {}
    for location, software in results:
        if location.id not in locations_software:
            locations_software[location.id] = {
                "location": location.put_into_dto(),
                "softwares": []
            }
        locations_software[location.id]["softwares"].append(software.put_into_dto())

    return make_response(jsonify(locations_software), HTTPStatus.OK)

@locations_bp.get('/capacity')
def get_location_capacity_stat() -> Response:
    """
    Gets Max, Min, Sum, or Avg for room_numbers from Locations table.
    The stat_type is passed as a query parameter (e.g., stat_type=MAX).
    """
    stat_type = request.args.get('stat_type').upper()
    result = get_location_stat(stat_type)

    if result != -1:
        return jsonify({stat_type: result})
    else:
        return jsonify({"error": "Invalid stat_type. Use MAX, MIN, SUM, or AVG"}), 400
