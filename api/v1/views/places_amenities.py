#!/usr/bin/python3
"""places amenities"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from os import environ

STORAGE_TYPE = environ.get('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """get amenity information"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place_amenities = []
    if STORAGE_TYPE == 'db':
        place_amenities_obj = place.amenities
    else:
        place_amenities_obj = place.amenities_ids
    for i in place_amenities_obj:
        place_amenities.append(i.to_dict())
    return jsonify(place_amenities)


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
    if STORAGE_TYPE == 'db':
        place_amenities_obj = place.amenities
    else:
        place_amenities_obj = place.amenities_ids
    if amenity not in place_amenities_obj:
        abort(404)
    place_amenities_obj.remove(amenity)
    place.save()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_amenity(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None:
        abort(404)
    if amenity is None:
        abort(404)
    if STORAGE_TYPE == 'db':
        place_amenities_obj = place.amenities
    else:
        place_amenities_obj = place.amenity_ids
    if amenity in place_amenities_obj:
        return jsonify(amenity.to_dict())
    place_amenities_obj.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
