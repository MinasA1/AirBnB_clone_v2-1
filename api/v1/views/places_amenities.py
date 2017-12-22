#!/usr/bin/python3
"""api.v1.views place_amenities"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE', 'POST'])
@app_views.route('/places/<place_id>/amenities/', methods=['GET'])
def get_places_amenities(place_id, amenity_id=None):
    """method to retrive all amenities for a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)
    if request.method is 'DELETE':
        if amenity.place_id is not place.id:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    if request.method is 'POST':
        if amenity.place_id is place.id:
            return jsonify(amenity.to_dict()), 200
        else:
            amenity.place_id = place.id
            return jsonify(amenity.to_dict()), 201
    amen = storage.all(Amenity)
    amenities = []
    for obj in amen:
        if amen[obj].place_id == place.id:
            amenities.append(amen[obj].to_dict())
    return jsonify(amenities), 200
