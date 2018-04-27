#!/usr/bin/python3
'''
   This module handles all default RestFul API actions for User objects.
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def all_users_by_state():
    '''
       Retrieves all User objects from storage
    '''
    users = storage.all("User")
    users_list = []
    for k, v in users.items():
        users_list.append(v.to_dict())

    return jsonify(users_list)


@app_views.route('/users/<uuid:user_id>', methods=['GET'],
                 strict_slashes=False)
def user_by_id(user_id):
    '''
       Retrieves a specified User object from storage
    '''
    try:
        user = storage.get("User", user_id)
        format_user = user.to_dict()
        return jsonify(format_user)
    except Exception:
        abort(404)


@app_views.route('/users/<uuid:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    '''
       Deletes a specified User object from storage
    '''
    try:
        user = storage.get("User", user_id)
        storage.delete(user)
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def create_user():
    '''
       Creates a new User object and saves it to storage
    '''
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})
    else:
        user_dict = request.get_json()
        if "email" not in user_dict:
            abort(400)
            return jsonify({"error": "Missing email"})
        elif "password" not in user_dict:
            abort(400)
            return jsonify({"error": "Missing password"})
        else:
            user_email = user_dict["email"]
            user_password = user_dict["password"]
            user = User(email=user_email, password=user_password)
            for k, v in user_dict.items():
                setattr(user, k, v)
            user.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<uuid:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    '''
       Updates an existing City object and saves it to storage
    '''
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    req = request.get_json()
    for k, v in req.items():
        if k != "id" and k != "created_at" and k != "updated_at" \
                and k != "email":
            setattr(user, k, v)
    user.save()

    return jsonify(user.to_dict()), 200
