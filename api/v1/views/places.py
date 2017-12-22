#!/usr/bin/python3
"""api.v1.views.place"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/places', methods=['GET', 'POST'],
                 defaults={'place_id': None})
def get_places(place_id):
    """method for retrieving, deleting, creating, updating place objects"""
    if place_id:
        place = storage.get(Place, place_id)  # retrieves obj
        if place is None:
            return jsonify({'error': 'Not found'}), 404
        if request.method == 'DELETE':
            storage.delete(place)  # deletes
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            js = request.get_json()
            if js is None:
                return jsonify({'error': 'Not a JSON'}), 400
            js.pop('id', None)
            js.pop('user_id', None)
            js.pop('city_id', None)
            js.pop('created_at', None)
            js.pop('updated_at', None)
            for key, value in js.items():
                setattr(place, key, value)  # updates
            place.save()
            return jsonify(place.to_dict()), 200
        else:
            return jsonify(place.to_dict()), 200

    if request.method == 'POST':
        js = request.get_json()
        if js is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if js.get('user_id', None) is None:
            return jsonify({'error': 'Missing user_id'}), 400
        if js.get('name', None) is None:
            return jsonify({'error': 'Missing name'}), 400
        obj = Place(**js)  # creates
        obj.save()
        return jsonify(obj.to_dict()), 201

    places = []
    places_obj = storage.all('Place')  # retrieves list obj
    for obj in places_obj:
        places.append(places_obj[obj].to_dict())
    return jsonify(places)
