#!/usr/bin/python3
"""places amenities"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """get amenity information"""
    place = storage.get_place(Place, place_id)
    if place is None:
        abort(404)
    amenities = [ameni.to_dict() for ameni in place.amenities]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenitiy(place_id, amenity_id):
    """delete amenities"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    

@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)