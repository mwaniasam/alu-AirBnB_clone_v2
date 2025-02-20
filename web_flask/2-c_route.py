#!/usr/bin/python3
""" 
Flask web application that starts a web server.

Routes:
- `/` : Displays "Hello HBNB!"
- `/hbnb` : Displays "HBNB"
- `/c/<text>` : Displays "C " followed by the value of `<text>`, 
  replacing underscores (`_`) with spaces.

The application listens on `0.0.0.0`, port `5000`.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Returns 'Hello HBNB!'"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Returns 'HBNB'"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """Returns 'C ' followed by `text`, replacing underscores with spaces"""
    return f"C {text.replace('_', ' ')}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
