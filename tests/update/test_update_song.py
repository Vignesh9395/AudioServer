import json
import os
import sys
import unittest
parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

sys.path.append(parent_dir)

from app import create_app

from flask import Flask


class TestUpdateSong(unittest.TestCase):

    # positive case
    def test_successful_update(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300
        }
        self.app.post('/song',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 350
        }
        # when
        response = self.app.put('/song/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("song with id {} updated".format(payload['id']),
                         json.loads(response.data)['message'])
        self.assertEqual(200, response.status_code)

    # negative cases
    def test_updating_non_existing_song(self):
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
        response = self.app.put('/song/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("A song with id '{}' does not exist.".format(payload['id']),
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

    def test_updating_song_id_mismatch(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload = {
            "id": 2,
            "name": "Enjoy Enjaami",
            "duration": 300
        }

        # when
        response = self.app.put('/song/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("song id '{0}' does not match with payload id '{1}'.".format(1, payload['id']),
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

    def test_wrong_id_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300
        }
        self.app.post('/song',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": "1",
            "name": "Enjoy Enjaami",
            "duration": 300
        }
        # when
        response = self.app.put('/song/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Song id of type integer is required!", json.loads(response.data)['message']['id'])
        self.assertEqual(400, response.status_code)

    def test_wrong_name_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300
        }
        self.app.post('/song',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "name": ["Enjoy Enjaami"],
            "duration": 300
        }
        # when
        response = self.app.put('/song/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Song name of type string upto 100 characters is required!",
                         json.loads(response.data)['message']['name'])
        self.assertEqual(400, response.status_code)

    def test_wrong_duration_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300
        }
        self.app.post('/song',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": "300"
        }
        # when
        response = self.app.put('/song/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Song Duration of type integer is required!", json.loads(response.data)['message']['duration'])
        self.assertEqual(400, response.status_code)

    def test_unknown_resource_update(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload1 = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300
        }
        self.app.post('/song/1',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload1))
        payload2 = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300
        }
        # when
        response = self.app.put('/songs/1',
                                headers={"Content-Type": "application/json"},
                                data=json.dumps(payload2))

        # Then
        self.assertEqual("No resource named songs exist.",
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

