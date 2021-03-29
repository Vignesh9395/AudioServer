import json
import os
import sys
import unittest
parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

sys.path.append(parent_dir)

from app import create_app

from flask import Flask


class TestUpdatePodcast(unittest.TestCase):

    # positive case
    def test_successful_update(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 350,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu", "anirudh"]
        }
        # when
        response = self.app.put('/podcast/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("podcast with id {} updated".format(payload['id']),
                         json.loads(response.data)['message'])
        self.assertEqual(200, response.status_code)

    # negative cases
    def test_updating_non_existing_podcast(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }

        # when
        response = self.app.put('/podcast/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("A podcast with id '{}' does not exist.".format(payload['id']),
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

    def test_updating_podcast_id_mismatch(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload = {
            "id": 2,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }

        # when
        response = self.app.put('/podcast/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("podcast id '{0}' does not match with payload id '{1}'.".format(1, payload['id']),
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
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": "1",
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu", "anirudh"]
        }
        # when
        response = self.app.put('/podcast/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Podcast id of type integer is required!", json.loads(response.data)['message']['id'])
        self.assertEqual(400, response.status_code)

    def test_wrong_name_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "name": ["Enjoy Enjaami"],
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu", "anirudh"]
        }
        # when
        response = self.app.put('/podcast/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Podcast name of type string upto 100 characters is required!",
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
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": "300",
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu", "anirudh"]
        }
        # when
        response = self.app.put('/podcast/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Podcast Duration of type integer is required!", json.loads(response.data)['message']['duration'])
        self.assertEqual(400, response.status_code)

    def test_wrong_host_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": 123,
            "participants": ["dhee", "arivu"]
        }
        # when
        response = self.app.put('/podcast/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Podcast Host of type string upto 100 characters is required!",
                         json.loads(response.data)['message']['host'])
        self.assertEqual(400, response.status_code)

    def test_wrong_participants_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": "dhee"
        }
        # when
        response = self.app.put('/podcast/1',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Podcast Participants should be a list of max 10 participants!",
                         json.loads(response.data)['message']['participants'])
        self.assertEqual(400, response.status_code)

    def test_wrong_participants_length(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]*6
        }
        # when
        response = self.app.post('/podcast',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Podcast Participants should be a list of max 10 participants!",
                         json.loads(response.data)['message']['participants'])
        self.assertEqual(400, response.status_code)

    def test_wrong_participant_type(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu", 123]
        }
        # when
        response = self.app.post('/podcast',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Podcast Participant name of type string upto 100 characters is required!",
                         json.loads(response.data)['message']['participants'])
        self.assertEqual(400, response.status_code)

    def test_wrong_participant_length(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload_input = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload_input))
        payload = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"*30]
        }
        # when
        response = self.app.post('/podcast',
                                 headers={"Content-Type": "application/json"},
                                 data=json.dumps(payload))

        # Then
        self.assertEqual("Podcast Participant name of type string upto 100 characters is required!",
                         json.loads(response.data)['message']['participants'])
        self.assertEqual(400, response.status_code)


    def test_unknown_resource_update(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        payload1 = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }
        self.app.post('/podcast/1',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload1))
        payload2 = {
            "id": 1,
            "name": "Enjoy Enjaami",
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu", "anirudh"]
        }
        # when
        response = self.app.put('/podcasts/1',
                                headers={"Content-Type": "application/json"},
                                data=json.dumps(payload2))

        # Then
        self.assertEqual("No resource named podcasts exist.",
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

