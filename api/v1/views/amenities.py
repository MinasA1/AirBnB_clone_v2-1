#!/usr/bin/python3
"""api.v1.views.amenity"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/amenities', methods=['GET', 'POST'],
                 defaults={'amenity_id': None})
def get_amenities(amenity_id):
    """method for retrieving, deleting, creating, updating amenity objects"""
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)  # retrieves obj
        if amenity is None:
            return jsonify({'error': 'Not found'}), 404
        if request.method == 'DELETE':
            storage.delete(amenity)  # deletes
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            js = request.get_json()
            if js is None:
                return jsonify({'error': 'Not a JSON'}), 400
            js.pop('id', None)
            js.pop('created_at', None)
            js.pop('updated_at', None)
            for key, value in js.items():
                setattr(amenity, key, value)  # updates
            amenity.save()
            return jsonify(amenity.to_dict()), 200
        else:
            return jsonify(amenity.to_dict()), 200

    if request.method == 'POST':
        js = request.get_json()
        if js is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if js.get('name', None) is None:
            return jsonify({'error': 'Missing name'}), 400
        obj = Amenity(**js)  # creates
        obj.save()
        return jsonify(obj.to_dict()), 201

    amenities = []
    amenities_obj = storage.all('Amenity')  # retrieves list obj
    for obj in amenities_obj:
        amenities.append(amenities_obj[obj].to_dict())
    return jsonify(amenities)
