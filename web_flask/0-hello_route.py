#!/usr/bin/python3
"""
A simple Flask web application that displays "Hello HBNB!" at the root URL.

This script starts a Flask web server listening on 0.0.0.0 (all available IP addresses)
on port 5000. When accessed at the root URL (/), it returns the text "Hello HBNB!".

Usage:
    Run this script directly to start the Flask server:
        $ python3 app.py

    The server will be accessible at http://0.0.0.0:5000/.
"""

from flask import Flask

# Create a Flask application
app = Flask(__name__)

# Define the route for the root URL (/)
@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Display 'Hello HBNB!' at the root URL."""
    return "Hello HBNB!"

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
