#!/usr/bin/python3
"""amenities"""

import re
from flask import abort, jsonify, make_response, request
from AirBnB_clone_v3.models import amenity
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """ get amenities"""
    get_amenitys = []
    for amenity in storage.all("Amenity").values():
        get_amenitys.append(amenity.to_dict())
    return jsonify(get_amenitys)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ get amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """create amenities"""
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    req_json = request.get_json()
    amenity = Amenity(**req_json)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """update amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    for a, v in request.get_json().items():
        if a not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, a, v)
    amenity.save()
    return jsonify(amenity.to_dict())
