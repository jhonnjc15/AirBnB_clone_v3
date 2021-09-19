#!/usr/bin/python3
"""
Route that return the status
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """
    function for status route that returns the status
    """
    response = {"status": "OK"}
    return jsonify(response)


@app_views.route('/stats')
def stats():
    """
    Endpoint that retrieves the number of each objects by type
    """
    response = {}
    classes = {
        "Amenity": "ameniies",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }
    for key, value in classes.items():
        response[value] = storage.count(key)
    return jsonify(response)
