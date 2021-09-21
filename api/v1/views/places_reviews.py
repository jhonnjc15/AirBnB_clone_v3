#!/usr/bin/python3
"""new view for Review object"""

from flask import abort, jsonify, make_response, request
from models import storage
from api.v1.views import app_views
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """get all review of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    get_reviews = []
    for review in place.reviews:
        get_reviews.append(review.to_dict())
    return jsonify(get_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """get a review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<places_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """create a review"""
    place = store.get(Place, place_id)
    if place is None:
        abort(404)
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in req_json:
        abort(400, 'Missing user_id')
    user = storage.get(User, req_json["user_id"])
    if user is None:
        abort(404)
    if 'text' not in req_json:
        abort(400, 'Missing text')
    review = Review(**req_json)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Update an existing review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    for a, v in request.get_json().items():
        if a not in ['id', 'user_id', 'place_id',
                     'created_at', 'updated_at']:
            setattr(review, a, v)
    review.save()
    return jsonify(review.to_dict())
