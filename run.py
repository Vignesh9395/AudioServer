"""
Author: Venkata Vignesh B

Description: Main route handler

            Call the application factory function to construct a Flask application
            instance using the default configuration
"""

from flask import Flask

from app import create_app, create_tables

if __name__ == '__main__':
    app = Flask(__name__)
    create_app(app)
    app.run(port=9935, debug=True)
    create_tables()
