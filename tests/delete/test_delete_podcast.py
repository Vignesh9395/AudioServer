import json
import os
import sys
import unittest
parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

sys.path.append(parent_dir)

from app import create_app

from flask import Flask


class TestDeletePodcast(unittest.TestCase):

    # positive cases
    def test_successful_delete_by_id(self):
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
        self.app.post('/podcast',
                     headers={"Content-Type": "application/json"},
                     data=json.dumps(payload))
        # when
        response = self.app.delete('/podcast/1')
        podcast = json.loads(response.data)
        # Then
        self.assertEqual("Deleted podcast with id 1", podcast['message'])
        self.assertEqual(200, response.status_code)

    # negative cases
    def test_unknown_podcast_delete_by_id(self):
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
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload1))
        # when
        response = self.app.delete('/podcast/2')

        # Then
        self.assertEqual("podcast with id {} not found".format(2),
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
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload1))
        # when
        response = self.app.delete('/podcasts/1')

        # Then
        self.assertEqual("No resource named podcasts exist.",
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)
