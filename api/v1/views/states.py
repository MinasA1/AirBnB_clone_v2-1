#!/usr/bin/env python3                                                                                                              """api.v1.views states"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/states/<state_id>', methods=['GET'])
@app_views.route('/states', methods=['GET'], defaults={'state_id': None})
def get_states(state_id):
    """status code"""
    if state_id:
        state = storage.get('State', state_id)
        return jsonify(state.to_dict())
    states = []
    states_obj = storage.all('State')
    for obj in states_obj:
        states.append(states_obj[obj].to_dict())
    return jsonify(states)
