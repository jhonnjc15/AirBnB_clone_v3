#!/usr/bin/python3
"""
Route that return the status
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """
    function for status route that returns the status
    """
    response = {"status": "OK"}
    return jsonify(response)
