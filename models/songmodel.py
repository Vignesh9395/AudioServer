"""
Author: Venkata Vignesh B

Description: Main Database service handler for Song Table
"""
from datetime import datetime
from db import db


class SongModel(db.Model):
    """
    Model Class for Song
    """
    __tablename__ = 'song'

    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False,
                              default=datetime.utcnow)

    def __init__(self, id, name, duration):
        """
        Constructor to initialize Song metadata
        """
        self.id = id
        self.name = name
        self.duration = duration

    def json(self):
        """
        Method to get Song metadata as json
        """
        return {
            'id': self.id,
            'name': self.name,
            'duration': self.duration,
            'uploaded_time': str(self.uploaded_time)
        }

    @classmethod
    def find_by_id(cls, id):
        """
                Method to get Song by id
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
                Method to save Song metadata to DB
                """
        if update:
            db.session.merge(self)
        else:
            db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
                Method to delete Song metadata from DB
                """
        db.session.delete(self)
        db.session.commit()