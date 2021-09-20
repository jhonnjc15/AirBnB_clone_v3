#!/usr/bin/python3
"""users"""


from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """get users information"""
    users = []
    for user in storage.all(User).values():
        user.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """get user information"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete user information"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """create user"""
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    if 'email' not in request.get_json:
        abort(400, 'Missing email')
    if 'password' not in request.get_json:
        abort(400, 'Missing password')
    req_json = request.get_json()
    user = User(**req_json)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """update user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    for a, v in request.get_json.items():
        if a not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, a, v)
    user.save()
    return jsonify(user.to_dict())
