#!/usr/bin/python3
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
