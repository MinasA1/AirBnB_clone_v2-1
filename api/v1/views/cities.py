#!/usr/bin/python3
"""api.v1.views.city"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/state/<state_id>/cities', methods=['GET', 'POST'])
def get_cities_state(state_id):
    """method to get cities for given state"""
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    if request.method == 'POST':
        js = request.get_json()
        if js is None:
            return jsonify({'error': 'Not JSON'}), 400
        if js.get('name', None) is None:
            return jsonify({'error': 'Missing name'}), 400
        city = City(**js)
        city.state_id = state.id
        city.save()
        return jsonify(city.to_dict()), 201
    cities = storage.all('City')
    match = []
    for city in cities:
        if cities[city].state_id == state.id:
            match.append(cities[city].to_dict())
    return jsonify(match), 200


@app_views.route('cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def get_city(city_id):
    """method to retrieve and delete City objects"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        js = request.get_json()
        if js is None:
            return jsonify({'error': 'Not a JSON'}), 400
        js.pop('id', None)
        js.pop('created_at', None)
        js.pop('updated_at', None)
        for key, value in js.items():
            setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    return jsonify(city.to_dict()), 200
