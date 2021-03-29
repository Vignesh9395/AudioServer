import json
import os
import sys
import unittest

parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

sys.path.append(parent_dir)

from app import create_app

from flask import Flask


class TestCreateAudiobook(unittest.TestCase):

    # positive case
    def test_successful_create(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }
        # when
        response = self.app.post('/audiobook',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))
        print(json.loads(response.data), response.status_code)
        # Then
        self.assertEqual("audiobook with id {} uploaded to server".format(payload['id']),
                         json.loads(response.data)['message'])
        self.assertEqual(200, response.status_code)

    # negative cases
    def test_creating_already_existing_Audiobook(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }

        inserted = self.app.post('/audiobook',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))
        # when
        response = self.app.post('/audiobook',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("A audiobook with id '{}' already exists.".format(payload['id']),
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

    def test_wrong_id_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload = {
            "id": "1",
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }
        # when
        response = self.app.post('/audiobook',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Audiobook id of type integer is required!", json.loads(response.data)['message']['id'])
        self.assertEqual(400, response.status_code)

    def test_wrong_title_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload = {
            "id": 1,
            "title": ["Enjoy Enjaami"],
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }
        # when
        response = self.app.post('/audiobook',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Audiobook title of type string upto 100 characters is required!",
                         json.loads(response.data)['message']['title'])
        self.assertEqual(400, response.status_code)

    def test_wrong_duration_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": "300",
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }
        # when
        response = self.app.post('/audiobook',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Audiobook Duration of type integer is required!",
                         json.loads(response.data)['message']['duration'])
        self.assertEqual(400, response.status_code)

    def test_wrong_author_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": 123,
            "narrator": "dhee"
        }
        # when
        response = self.app.post('/audiobook',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Audiobook author of type string upto 100 characters is required!",
                         json.loads(response.data)['message']['author'])
        self.assertEqual(400, response.status_code)

    def test_wrong_narrator_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": ["dhee"]
        }
        # when
        response = self.app.post('/audiobook',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Audiobook narrator of type string upto 100 characters is required!",
                         json.loads(response.data)['message']['narrator'])
        self.assertEqual(400, response.status_code)
