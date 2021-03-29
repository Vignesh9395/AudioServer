import json
import os
import sys
import unittest
parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

sys.path.append(parent_dir)

from app import create_app

from flask import Flask


class TestUpdateAudiobook(unittest.TestCase):

    # positive case
    def test_successful_update(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }
        self.app.post('/audiobook',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 350,
            "author": "santhosh narayanan",
            "narrator": "arivu"
        }
        # when
        response = self.app.put('/audiobook/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("audiobook with id {} updated".format(payload['id']),
                         json.loads(response.data)['message'])
        self.assertEqual(200, response.status_code)

    # negative cases
    def test_updating_non_existing_audiobook(self):
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
        response = self.app.put('/audiobook/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("A audiobook with id '{}' does not exist.".format(payload['id']),
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

    def test_updating_audiobook_id_mismatch(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload = {
            "id": 2,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }

        # when
        response = self.app.put('/audiobook/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("audiobook id '{0}' does not match with payload id '{1}'.".format(1, payload['id']),
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

    def test_wrong_id_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }
        self.app.post('/audiobook',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": "1",
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "arivu"
        }
        # when
        response = self.app.put('/audiobook/1',
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
        payload_input = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }
        self.app.post('/audiobook',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "title": ["Enjoy Enjaami"],
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "arivu"
        }
        # when
        response = self.app.put('/audiobook/1',
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
        payload_input = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }
        self.app.post('/audiobook',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": "300",
            "author": "santhosh narayanan",
            "narrator": "arivu"
        }
        # when
        response = self.app.put('/audiobook/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Audiobook Duration of type integer is required!", json.loads(response.data)['message']['duration'])
        self.assertEqual(400, response.status_code)

    def test_wrong_author_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }
        self.app.post('/audiobook',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": 123,
            "narrator": "dhee"
        }
        # when
        response = self.app.put('/audiobook/1',
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
        payload_input = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }
        self.app.post('/audiobook',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": ["dhee"]
        }
        # when
        response = self.app.put('/audiobook/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Audiobook narrator of type string upto 100 characters is required!",
                         json.loads(response.data)['message']['narrator'])
        self.assertEqual(400, response.status_code)

    def test_unknown_resource_update(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload1 = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "dhee"
        }
        self.app.post('/audiobook/1',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload1))
        payload2 = {
            "id": 1,
            "title": "Enjoy Enjaami",
            "duration": 300,
            "author": "santhosh narayanan",
            "narrator": "arivu"
        }
        # when
        response = self.app.put('/audiobooks/1',
                                headers={"Content-Type": "application/json"},
                                data=json.dumps(payload2))

        # Then
        self.assertEqual("No resource named audiobooks exist.",
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

