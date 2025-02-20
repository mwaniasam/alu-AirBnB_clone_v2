#!/usr/bin/python3
"""
This module starts a Flask web application.

The application listens on `0.0.0.0`, port `5000`.

Routes:
    /                     -> Displays "Hello HBNB!"
    /hbnb                 -> Displays "HBNB"
    /c/<text>             -> Displays "C " followed by the value of `text`,
                             replacing underscores (_) with spaces.
    /python/(<text>)      -> Displays "Python " followed by the value of `text`,
                             replacing underscores (_) with spaces.
                             The default value of `text` is "is cool".
    /number/<n>           -> Displays "<n> is a number" only if `n` is an integer.
    /number_template/<n>  -> Displays an HTML page with:
                             "<h1>Number: n</h1>" inside the body, only if `n` is an integer.
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Returns:
        str: "Hello HBNB!"
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Returns:
        str: "HBNB"
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """
    Displays 'C ' followed by the value of `text`,
    replacing underscores with spaces.

    Args:
        text (str): The text to display.

    Returns:
        str: The formatted string.
    """
    return f"C {text.replace('_', ' ')}"


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python_text(text="is cool"):
    """
    Displays 'Python ' followed by the value of `text`,
    replacing underscores with spaces.

    Args:
        text (str, optional): The text to display. Defaults to "is cool".

    Returns:
        str: The formatted string.
    """
    return f"Python {text.replace('_', ' ')}"


@app.route('/number/<int:n>', strict_slashes=False)
def is_number(n):
    """
    Displays '<n> is a number' only if `n` is an integer.

    Args:
        n (int): The number to display.

    Returns:
        str: The formatted string.
    """
    return f"{n} is a number"


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_template(n):
    """
    Displays an HTML page with "<h1>Number: n</h1>" inside the body
    only if `n` is an integer.

    Args:
        n (int): The number to display.

    Returns:
        str: Rendered HTML template.
    """
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
