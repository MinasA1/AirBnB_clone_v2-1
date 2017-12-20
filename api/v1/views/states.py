#!/usr/bin/env python3
"""api.v1.views states"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/states', methods=['GET', 'POST'],
                 defaults={'state_id': None})
def get_states(state_id):
    """states method for retrieving and deleting State objects """
    if request.method == 'POST':
        js = request.get_json()
        if js is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if js.get('name', None) is None:
            return jsonify({'error': 'Missing name'}), 400
        obj = State(**js)
        obj.save()
        return jsonify(obj.to_dict()), 200

    if state_id:
        state = storage.get('State', state_id)
        if state is None:
            return jsonify({'error': 'Not found'}), 404
        if request.method == 'DELETE':
            storage.delete(state)
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            js = request.get_json()
            if js is None:
                return jsonify({'error': 'Not a JSON'}), 400
            js.pop('id', None)
            js.pop('created_at', None)
            js.pop('updated_at', None)
            for k, v in js.items():
                setattr(state, k, v)
            state.save()
            return jsonify(state.to_dict()), 200
        else:
            return jsonify(state.to_dict())
    states = []
    states_obj = storage.all('State')
    for obj in states_obj:
        states.append(states_obj[obj].to_dict())
    return jsonify(states)
