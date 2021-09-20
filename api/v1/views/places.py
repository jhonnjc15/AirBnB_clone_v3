#!/usr/bin/python3
"""users"""


from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User
from models.place import Place
from models.city import City
from api.v1.views import app_views


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Get a list of places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [plc.to_dict() for plc in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_places(state_id):
    """get places information"""
    place = storage.get(Place, state_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Create a new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    req_json = request.get_json()
    req_json['city_id'] = city_id
    user = storage.get(User, req_json['user_id'])
    if user is None:
        abort(404)
    place = Place(**req_json)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Update an existing place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    for a, v in request.get_json().items():
        if a not in ['id', 'user_id', 'city_id',
                     'created_at', 'updated_at']:
            setattr(place, a, v)
    place.save()
    return jsonify(place.to_dict())
