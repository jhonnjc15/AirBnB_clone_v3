#!/usr/bin/python3
"""
Flask app
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """
    After each request, this method calls .close()
    """
    storage.close()


@app.errorhandler(404)
def handle_not_found(err):
    """Return JSON instead of HTML for any other server error"""
    response = {"error": "Not found"}
    return jsonify(response), 404

if __name__ == "__main__":
    app.run(host=host, port=port, threaded=True)
