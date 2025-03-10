#!/usr/bin/python3
"""
Flask web application that defines two routes:
- `/` displays "Hello HBNB!"
- `/hbnb` displays "HBNB"
The application listens on 0.0.0.0, port 5000.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Returns the string 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Returns the string 'HBNB'"""
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
