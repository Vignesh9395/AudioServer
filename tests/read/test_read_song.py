import json
import os
import sys
import unittest
parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

sys.path.append(parent_dir)

from app import create_app

from flask import Flask


class TestReadSong(unittest.TestCase):

    # positive cases
    def test_successful_read_empty(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        # empty db

        # when
        response = self.app.get('/song')

        # Then
        self.assertListEqual([], json.loads(response.data)['songs'])
        self.assertEqual(200, response.status_code)

    def test_successful_read_all(self):
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
        payload2 = {
            "id": 2,
            "name": "kutty story",
            "duration": 250
        }
        self.app.post('/song',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload2))
        # when
        response = self.app.get('/song')
        songs = json.loads(response.data)['songs']
        songs[0].pop('upload_time')
        songs[1].pop('upload_time')
        # Then
        self.assertDictEqual(payload1,
                             songs[0])
        self.assertDictEqual(payload2,
                             songs[1])
        self.assertEqual(200, response.status_code)

    def test_successful_read_by_id(self):
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
        response = self.app.get('/song/1')
        song = json.loads(response.data)
        song.pop('upload_time')
        # Then
        self.assertDictEqual(payload, song)
        self.assertEqual(200, response.status_code)

    # negative cases
    def test_unknown_song_read_by_id(self):
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
        response = self.app.get('/song/2')

        # Then
        self.assertEqual("song with id {} not found".format(2),
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

    def test_unknown_resource_read(self):
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
        response = self.app.get('/songs')

        # Then
        self.assertEqual("No resource named songs exist.",
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)
