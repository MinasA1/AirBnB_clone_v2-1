#!/usr/bin/env python3                                                                                                              """api.v1.views index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """status code"""
    return jsonify({'status':'OK'})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """number of each obj"""
    names = { 'Amenity': 'amenities', 'City': 'cities', 'Place': 'places',
              'Review': 'reviews', 'State': 'states', 'User': 'users'}
    d = {}
    for n in names:
        d[names[n]] = storage.count(n)
    return jsonify(d)
