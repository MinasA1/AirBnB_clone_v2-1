#!/usr/bin/env python3
"""api app"""
from sys import path
path.insert(0, "../")
from models import storage
from api.v1.views import app_views
from flask import Flask, render_template
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(self):
    """call storage.close()"""
    storage.close()

if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', default='0.0.0.0'),
            port=getenv('HBNB_API_PORT', default=5000))
