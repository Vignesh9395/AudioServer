"""
Author: Venkata Vignesh B

Description: Main route handler
            Registers all resources with routes and creates the database
"""

from flask_restful import Api

from db import db

# import audio CRUD resources
from resources.audioserver import CreateAudio, GetAudio, UpdateAudio, DeleteAudio


def create_tables():
    """
            Method to create all tables from schema
        """
    db.create_all()


def initialize_routes(api):
    """
        Method to register all resources with routes
        """
    api.add_resource(CreateAudio, '/<string:audioFileType>')
    api.add_resource(GetAudio, '/<path:path>')
    api.add_resource(UpdateAudio, '/<string:audioFileType>/<int:audioFileID>')
    api.add_resource(DeleteAudio, '/<string:audioFileType>/<int:audioFileID>')


def initialize_db(app):
    """
            Method to initialize db
        """
    db.init_app(app)


def create_app(app, sql_path=None):
    """
            Method to initialize_routes, db and create tables for use
        """
    app.config['SQLALCHEMY_DATABASE_URI'] = sql_path or 'sqlite:///data.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True
    api = Api(app)
    initialize_db(app)
    initialize_routes(api)
    with app.app_context():
        create_tables()