#!/usr/bin/python3
"""api.v1.views.places_reviews"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/places_reviews',
                 methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/places_reviews', methods=['GET', 'POST'],
                 defaults={'review_id': None})
def get_reviews(review_id):
    """method for retrieving, deleting, creating, updating review objects"""
    if review_id:
        review = storage.get(Review, review_id)  # retrieves obj
        if review is None:
            return jsonify({'error': 'Not found'}), 404
        if request.method == 'DELETE':
            storage.delete(review)  # deletes
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            js = request.get_json()
            if js is None:
                return jsonify({'error': 'Not a JSON'}), 400
            js.pop('id', None)
            js.pop('user_id', None)
            js.pop('place_id', None)
            js.pop('created_at', None)
            js.pop('updated_at', None)
            for key, value in js.items():
                setattr(review, key, value)  # updates
            review.save()
            return jsonify(review.to_dict()), 200
        else:
            return jsonify(review.to_dict()), 200

    if request.method == 'POST':
        js = request.get_json()
        if js is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if js.get('user_id', None) is None:
            return jsonify({'error': 'Missing user_id'}), 400
        if js.get('text', None) is None:
            return jsonify({'error': 'Missing text'}), 400
        obj = Review(**js)  # creates
        obj.save()
        return jsonify(obj.to_dict()), 201

    reviews = []
    reviews_obj = storage.all('Review')  # retrieves list obj
    for obj in reviews_obj:
        reviews.append(reviews_obj[obj].to_dict())
    return jsonify(reviews)
