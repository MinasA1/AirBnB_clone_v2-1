#!/usr/bin/env python3                                                                                                              """api.v1.views index"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """status code"""
    return jsonify({'status':'OK'})
