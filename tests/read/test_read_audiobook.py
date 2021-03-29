import json
import os
import sys
import unittest
parent_dir = os.path.dirname(os.path.dirname(os.getcwd()))

sys.path.append(parent_dir)

from app import create_app

from flask import Flask


class TestReadAudiobook(unittest.TestCase):

    # positive cases
    def test_successful_read_empty(self):
        app = Flask(__name__)
        create_app(app, sql_path='sqlite:///')
        self.app = app.test_client()
        # given
        # empty db

        # when
        response = self.app.get('/audiobook')

        # Then
        self.assertListEqual([], json.loads(response.data)['audiobooks'])
        self.assertEqual(200, response.status_code)

    def test_successful_read_all(self):
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

        self.app.post('/audiobook',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload1))
        payload2 = {
            "id": 2,
            "title": "kutty story",
            "duration": 250,
            "author": "anirudh",
            "narrator": "vijay"
        }
        self.app.post('/audiobook',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload2))

        # when
        response = self.app.get('/audiobook')
        audiobooks = json.loads(response.data)['audiobooks']
        print(audiobooks)
        audiobooks[0].pop('uploaded_time')
        audiobooks[1].pop('uploaded_time')
        # Then
        self.assertDictEqual(payload1,
                             audiobooks[0])
        self.assertDictEqual(payload2,
                             audiobooks[1])
        self.assertEqual(200, response.status_code)

    def test_successful_read_by_id(self):
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
        self.app.post('/audiobook',
                     headers={"Content-Type": "application/json"},
                     data=json.dumps(payload))
        # when
        response = self.app.get('/audiobook/1')
        audiobook = json.loads(response.data)
        audiobook.pop('uploaded_time')
        # Then
        self.assertDictEqual(payload, audiobook)
        self.assertEqual(200, response.status_code)

    # negative cases
    def test_unknown_audiobook_read_by_id(self):
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
        self.app.post('/audiobook',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload1))
        # when
        response = self.app.get('/audiobook/2')

        # Then
        self.assertEqual("audiobook with id {} not found".format(2),
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

    def test_unknown_resource_read(self):
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
        self.app.post('/audiobook',
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(payload1))
        # when
        response = self.app.get('/audiobooks')

        # Then
        self.assertEqual("No resource named audiobooks exist.",
                         json.loads(response.data)['message'])
        self.assertEqual(400, response.status_code)

