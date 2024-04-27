#!/usr/bin/python3
"""
Begins a Flask web application.
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """Responds with Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Responds with HBNB"""
    return 'HBNB'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

