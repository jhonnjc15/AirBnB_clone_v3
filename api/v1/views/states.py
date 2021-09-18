#!/usr/bin/python3

from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from api.v1.views import app_views

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    states = []
    for state in storage.all("State").values():
        states.append(state.to_dict())
    return jsonify(state)


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id):
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())
