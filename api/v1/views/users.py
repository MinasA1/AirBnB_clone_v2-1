#!/usr/bin/python3
"""api.v1.views.user"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'])
@app_views.route('/users', methods=['GET', 'POST'],
                 defaults={'user_id': None})
def get_users(user_id):
    """method for retrieving, deleting, creating, updating user objects"""
    if user_id:
        user = storage.get(User, user_id)  # retrieves obj
        if user is None:
            return jsonify({'error': 'Not found'}), 404
        if request.method == 'DELETE':
            storage.delete(user)  # deletes
            storage.save()
            return jsonify({}), 200
        elif request.method == 'PUT':
            js = request.get_json()
            if js is None:
                return jsonify({'error': 'Not a JSON'}), 400
            js.pop('id', None)
            js.pop('email', None)
            js.pop('created_at', None)
            js.pop('updated_at', None)
            for key, value in js.items():
                setattr(user, key, value)  # updates
            user.save()
            return jsonify(user.to_dict()), 200
        else:
            return jsonify(user.to_dict()), 200

    if request.method == 'POST':
        js = request.get_json()
        if js is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if js.get('email', None) is None and js.get('password', None) is None:
            return jsonify({'error': 'Missing name'}), 400
        obj = User(**js)  # creates
        obj.save()
        return jsonify(obj.to_dict()), 201

    users = []
    users_obj = storage.all('User')  # retrieves list obj
    for obj in users_obj:
        users.append(users_obj[obj].to_dict())
    return jsonify(users)
