#!/usr/bin/python3
"""cities"""

from flask import abort, jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """get_cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [cit.to_dict() for cit in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """get_cities"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """create city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    req_json = request.get_json()
    req_json['state_id'] = state_id
    city = City(**req_json)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """update city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    for a, v in request.get_json().items():
        if a not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, a, v)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
