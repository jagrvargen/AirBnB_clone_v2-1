'''
   This module creates a route /status on the object app_views that returns a
   JSON
'''
from flask import jsonify
from api.v1.views import app_views
import models


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    stat_dict = {}
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    class_names = ['amenities', 'cities', 'places', 'reviews', 'states',
                   'users']

    for cls in range(len(classes)):
        stat_dict[class_names[cls]] = models.storage.count(classes[cls])
    return jsonify(stat_dict)
