#!/usr/bin/python3
"""
Defines a Flask web application
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """Handles the root route, returns 'Hello HBNB!'"""
    return 'Hello HBNB!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')  # Starts the application on host 0.0.0.0 and port 5000

