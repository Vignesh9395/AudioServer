"""
Author: Venkata Vignesh B

Description: Main Database service handler for Podcast Table
"""
from datetime import datetime
import ast
from db import db


class PodcastModel(db.Model):
    """
        Model Class for Podcast
        """
    __tablename__ = 'podcast'

    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False,
                              default=datetime.utcnow)
    host = db.Column(db.String(100), nullable=False)
    participants = db.Column(db.String(1100), nullable=True)

    def __init__(self, id, name, duration, host, participants):
        """
                Constructor to initialize Podcast metadata
                """
        self.id = id
        self.name = name
        self.duration = duration
        self.host = host
        self.participants = str(participants)

    def json(self):
        """
                Method to get Podcast metadata as json
                """
        return {
            'id': self.id,
            'name': self.name,
            'duration': self.duration,
            'uploaded_time': str(self.uploaded_time),
            'host': self.host,
            'participants': ast.literal_eval(self.participants)
        }

    @classmethod
    def find_by_id(cls, id):
        """
                        Method to get Podcast by id
                        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        """
                        Method to get all Song metadata
                        """
        return cls.query.all()

    def save_to_db(self, update=False):
        """
                        Method to save Podcast metadata to DB
                        """
        if update:
            db.session.merge(self)
        else:
            db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
                        Method to delete Podcast metadata from DB
                        """
        db.session.delete(self)
        db.session.commit()