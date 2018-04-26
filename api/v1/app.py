#!/usr/bin/python3
'''
   This module contains a Flask instance
'''
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
host = os.getenv('HBNB_API_HOST', default='0.0.0.0')
port = int(os.getenv('HBNB_API_PORT', default=5000))


@app.teardown_appcontext
def teardown_db(self):
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    app.run(host=host, port=port)
