#!/usr/bin/python3
'''
   This module handles all default RestFul API actions for Place objects.
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import Place


@app_views.route('/cities/<uuid:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places_by_city(city_id):
    '''
       Retrieves all Place objects from storage that belong to specified City
    '''
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    places_list = []
    places = storage.all("Place")
    for k, v in places.items():
        if v.city_id == str(city_id):
            places_list.append(v.to_dict())

    return jsonify(places_list)


@app_views.route('/places/<uuid:place_id>', methods=['GET'],
                 strict_slashes=False)
def place_by_id(place_id):
    '''
       Retrieves a specified Place object from storage
    '''
    try:
        place = storage.get("Place", place_id)
        format_place = place.to_dict()
        return jsonify(format_place)
    except Exception:
        abort(404)


@app_views.route('/places/<uuid:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''
       Deletes a specified Place object from storage
    '''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    else:
        storage.delete(place)
        return jsonify({}), 200


@app_views.route('/cities/<uuid:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''
       Creates a new Place object and saves it to storage
    '''
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    place_dict = request.get_json()
    if "user_id" not in place_dict:
        abort(400)
        return jsonify({"error": "Missing user_id"})
    elif "name" not in place_dict:
        abort(400)
        return jsonify({"error": "Missing name"})

    # Check that user_id is linked to actual User object
    user_check = storage.get("User", place_dict["user_id"])
    if not user_check:
        abort(404)

    place_name = place_dict["name"]
    user_id = place_dict["user_id"]
    place = Place(name=place_name, user_id=user_id, city_id=city_id)
    for k, v in place_dict.items():
        setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<uuid:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    '''
       Updates an existing Place object and saves it to storage
    '''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    req = request.get_json()
    for k, v in req.items():
        if k != "id" and k != "created_at" and k != "updated_at" and \
                k != "user_id" and k != "city_id":
            setattr(place, k, v)
    place.save()

    return jsonify(place.to_dict()), 200
