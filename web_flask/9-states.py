#!/usr/bin/python3
"""
Initiates a Flask web application
"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/states', strict_slashes=False)
@app.route('/states/<state_id>', strict_slashes=False)
def states(state_id=None):
    """Displays the states and cities listed in alphabetical order"""
    # Retrieves all states from the storage
    states = storage.all("State")
    # Checks if state_id is provided
    if state_id is not None:
        # Prepares the state_id for retrieval
        state_id = 'State.' + state_id
    # Renders the HTML template with states data
    return render_template('9-states.html', states=states, state_id=state_id)


@app.teardown_appcontext
def teardown_db(exception):
    """Closes the storage connection upon teardown"""
    # Closes the storage connection
    storage.close()

if __name__ == '__main__':
    # Runs the Flask application
    app.run(host='0.0.0.0', port='5000')

