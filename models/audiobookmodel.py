"""
Author: Venkata Vignesh B

Description: Main Database service handler for Audiobook Table
"""
from datetime import datetime
from db import db


class AudiobookModel(db.Model):
    """
            Model Class for Audiobook
            """
    __tabletitle__ = 'audiobook'

    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    narrator = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(db.DateTime, nullable=False,
                              default=datetime.utcnow)

    def __init__(self, id, title, author, narrator, duration):
        """
                Constructor to initialize Audiobook metadata
                """
        self.id = id
        self.title = title
        self.author = author
        self.narrator = narrator
        self.duration = duration

    def json(self):
        """
                Method to get Audiobook metadata as json
                """
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'narrator': self.narrator,
            'duration': self.duration,
            'uploaded_time': str(self.uploaded_time)
        }

    @classmethod
    def find_by_id(cls, id):
        """
                        Method to get Audiobook by id
                        """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        """
                        Method to get all Audiobook metadata
                        """
        return cls.query.all()

    def save_to_db(self, update=False):
        """
                        Method to save Audiobook metadata to DB
                        """
        if update:
            db.session.merge(self)
        else:
            db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
                        Method to delete Audiobook metadata from DB
                        """
        db.session.delete(self)
        db.session.commit()