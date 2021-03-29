import json
import os
import sys
import unittest
parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

sys.path.append(parent_dir)

from app import create_app

from flask import Flask


class TestReadPodcast(unittest.TestCase):

    # positive cases
    def test_successful_read_empty(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        # empty db

        # when
        response = self.app.get('/podcast')

        # Then
        self.assertListEqual([], json.loads(response.data)['podcasts'])
        self.assertEqual(200, response.status_code)

    def test_successful_read_all(self):
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
        payload2 = {
            "id": 2,
            "name": "kutty story",
            "duration": 250,
            "host": "anirudh",
            "participants": ["vijay", "anirudh"]
        }
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload2))

        # when
        response = self.app.get('/podcast')
        podcasts = json.loads(response.data)['podcasts']
        print(podcasts)
        podcasts[0].pop('uploaded_time')
        podcasts[1].pop('uploaded_time')
        # Then
        self.assertDictEqual(payload1,
                             podcasts[0])
        self.assertDictEqual(payload2,
                             podcasts[1])
        self.assertEqual(200, response.status_code)

    def test_successful_read_by_id(self):
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
        response = self.app.get('/podcast/1')
        podcast = json.loads(response.data)
        podcast.pop('uploaded_time')
        # Then
        self.assertDictEqual(payload, podcast)
        self.assertEqual(200, response.status_code)

    # negative cases
    def test_unknown_podcast_read_by_id(self):
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
        response = self.app.get('/podcast/2')

        # Then
        self.assertEqual("podcast with id {} not found".format(2),
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
            "duration": 300,
            "host": "santhosh narayanan",
            "participants": ["dhee", "arivu"]
        }
        self.app.post('/podcast',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload1))
        # when
        response = self.app.get('/podcasts')

        # Then
        self.assertEqual("No resource named podcasts exist.",
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)
