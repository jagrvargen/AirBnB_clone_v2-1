#!/usr/bin/python3
'''
   This module handles all default RestFul API actions for State objects.
'''
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import State


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def all_states():
    '''
       Retrieves all State objects from storage
    '''
    states_list = []
    states = storage.all("State")
    for k, v in states.items():
        states_list.append(v.to_dict())

    return jsonify(states_list)


@app_views.route('/states/<uuid:state_id>', methods=['GET'],
                 strict_slashes=False)
def state_by_id(state_id):
    '''
       Retrieves a specified State object from storage
    '''
    try:
        state = storage.get("State", state_id)
        format_state = state.to_dict()
        return jsonify(format_state)
    except Exception:
        abort(404)


@app_views.route('/states/<uuid:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    '''
       Deletes a specified State object from storage
    '''
    try:
        state = storage.get("State", state_id)
        storage.delete(state)
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''
       Creates a new State object and saves it to storage
    '''
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})
    else:
        state_dict = request.get_json()
        if "name" in state_dict:
            state_name = state_dict["name"]
            state = State(name=state_name)
            for k, v in state_dict.items():
                setattr(state, k, v)
            state.save()
        else:
            abort(400)
            return jsonify({"error": "Missing name"})
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<uuid:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    '''
       Updates an existing State object and saves it to storage
    '''
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400)
        return jsonify({"error": "Not a JSON"})

    req = request.get_json()
    for k, v in req.items():
        if k != "id" and k != "created_at" and k != "updated_at":
            setattr(state, k, v)
    state.save()

    return jsonify(state.to_dict()), 200
