import json
import os
import sys
import unittest
parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

sys.path.append(parent_dir)

from app import create_app

from flask import Flask


class TestDeleteSong(unittest.TestCase):

    # positive cases
    def test_successful_delete_by_id(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300
        }
        # when
        self.app.post('/song',
                     headers={"Content-Type": "application/json"},
                     data=json.dumps(payload))
        # when
        response = self.app.delete('/song/1')
        song = json.loads(response.data)
        # Then
        self.assertEqual("Deleted song with id 1", song['message'])
        self.assertEqual(200, response.status_code)

    # negative cases
    def test_unknown_song_delete_by_id(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload1 = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300
        }
        self.app.post('/song',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload1))
        # when
        response = self.app.delete('/song/2')

        # Then
        self.assertEqual("song with id {} not found".format(2),
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

    def test_unknown_resource_delete(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload1 = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300
        }
        self.app.post('/song',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload1))
        # when
        response = self.app.delete('/songs/1')

        # Then
        self.assertEqual("No resource named songs exist.",
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)
