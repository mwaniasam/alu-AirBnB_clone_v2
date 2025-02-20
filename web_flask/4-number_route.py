#!/usr/bin/python3
"""Flask web application that starts a web server.

Routes:
- `/` : Displays "Hello HBNB!"
- `/hbnb` : Displays "HBNB"
- `/c/<text>` : Displays "C " followed by the value of `<text>`,
  replacing underscores (`_`) with spaces.
- `/python/(<text>)` : Displays "Python " followed by the value of `<text>`,
  replacing underscores (`_`) with spaces. The default value of `<text>` is "is cool".
- `/number/<n>` : Displays "<n> is a number" only if `<n>` is an integer.

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


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """Returns 'Python ' followed by `text`, replacing underscores with spaces"""
    return f"Python {text.replace('_', ' ')}"


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """Returns '<n> is a number' only if `n` is an integer"""
    return f"{n} is a number"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
