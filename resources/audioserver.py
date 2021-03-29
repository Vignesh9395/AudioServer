"""
Author: Venkata Vignesh B

Description: Main service handler
"""

from flask import jsonify, make_response
from flask_restful import Resource

from models.audiobookmodel import AudiobookModel
from models.podcastmodel import PodcastModel
from models.songmodel import SongModel
from resources.audiobook import Audiobook
from resources.podcast import Podcast
from resources.song import Song

RESOURCE_MAP = {'song': Song, 'podcast': Podcast, 'audiobook': Audiobook}

MODEL_MAP = {'song': SongModel, 'podcast': PodcastModel, 'audiobook': AudiobookModel}


def format_response(message, status):
    """
            Method to format responses 
        """
    response = make_response(
        jsonify(
            {"message": message}
        ),
        status,
    )
    response.headers["Content-Type"] = "application/json"
    return response


def format_content(message, status):
    """
                Method to format response content
            """
    content = make_response(
        jsonify(
            message
        ),
        status,
    )
    content.headers["Content-Type"] = "application/json"
    return content


class CreateAudio(Resource):
    """
            Create audio resource endpoint.
            ---
            post:
              description: Create specific audio file
              parameters:
              content:
                application/json:
                    schema: [Song, Audiobook, Podcast]
              responses:
                200:
                  description: Creates new specific audio file
                  content:
                    application/json
        """

    def post(self, audio_file_type: str):
        """
                 Method to handle post request
                """

        if audio_file_type not in RESOURCE_MAP:
            message = "No resource named {0} exist.".format(audio_file_type)
            return format_response(message, 400)
        audio_resource = RESOURCE_MAP[audio_file_type]

        audio_model = MODEL_MAP[audio_file_type]

        data = audio_resource.parser.parse_args(strict=True)

        audio_id = data['id']

        if audio_model.find_by_id(audio_id):
            message = "A {0} with id '{1}' already exists.".format(audio_file_type, audio_id)
            return format_response(message, 400)

        audio = audio_model(**data)

        try:
            audio.save_to_db()
        except Exception as e:
            print(f'{e}')
            message = "An error occurred while uploading the {}.".format(audio_file_type)
            return format_response(message, 400)
        message = "{0} with id {1} uploaded to server".format(audio_file_type, audio_id)
        return format_response(message, 200)


class GetAudio(Resource):
    """
                Read audio resource endpoint.
                ---
                get:
                  description: Get specific audio file
                  responses:
                    200:
                      description: Return the specific audio file
                      content:
                        application/json:
                          schema: [Song, Audiobook, Podcast]
            """

    def get(self, path):

        """
                 Method to handle get request
                """
        if len(path.split('/')) > 1:
            audio_file_type, audio_file_id = path.split('/')
        else:
            audio_file_type, audio_file_id = path.split('/')[0], None

        if audio_file_type not in RESOURCE_MAP:
            message = "No resource named {0} exist.".format(audio_file_type)
            return format_response(message, 400)

        audio_model = MODEL_MAP[audio_file_type]

        if audio_file_id is None:
            audio_files = [audio_file.json() for audio_file in audio_model.find_all()]
            message = {'{}'.format(audio_file_type + 's'): audio_files}
            return format_content(message, 200)
        audio_file = audio_model.find_by_id(audio_file_id)
        if audio_file:
            message = audio_file.json()
            return format_content(message, 200)
        message = '{0} with id {1} not found'.format(audio_file_type, audio_file_id)
        return format_response(message, 400)


class UpdateAudio(Resource):
    """
                Update audio resource endpoint.
                ---
                put:
                  description: Update specific audio file
                  parameters:
                  content:
                    application/json:
                        schema: [Song, Audiobook, Podcast]
                  responses:
                    200:
                      description: Updates existing specific audio file
                      content:
                        application/json
            """

    def put(self, audio_file_type: str, audio_file_id: int):

        """
                 Method to handle put request
                """

        if audio_file_type not in RESOURCE_MAP:
            message = "No resource named {0} exist.".format(audio_file_type)
            return format_response(message, 400)

        audio_resource = RESOURCE_MAP[audio_file_type]

        audio_model = MODEL_MAP[audio_file_type]

        data = audio_resource.parser.parse_args(strict=True)

        audio_id = audio_file_id

        audio = audio_model.find_by_id(audio_id)

        if audio_id == data['id']:
            if audio:
                audio = audio_model(**data)

                try:
                    audio.save_to_db(update=True)
                except Exception as e:
                    print(e)
                    message = "An error occurred while updating the {}.".format(audio_file_type)
                    return format_response(message, 500)
            else:
                message = "A {0} with id '{1}' does not exist.".format(audio_file_type, audio_id)
                return format_response(message, 400)
        else:
            message = "{0} id '{1}' does not match with payload id '{2}'."\
                .format(audio_file_type, audio_id, data['id'])
            return format_response(message, 400)

        message = "{0} with id {1} updated".format(audio_file_type, audio_id)
        return format_response(message, 200)


class DeleteAudio(Resource):
    """
                Delete audio resource endpoint.
                ---
                get:
                  description: Delete specific audio file
                  responses:
                    200:
                      description: Delete the specific audio file
                      content:
                        application/json
            """

    def delete(self, audio_file_type: str, audio_file_id: int):

        """
                 Method to handle delete request
                """

        if audio_file_type not in RESOURCE_MAP:
            message = "No resource named {0} exist.".format(audio_file_type)
            return format_response(message, 400)

        audio_model = MODEL_MAP[audio_file_type]

        audio_file = audio_model.find_by_id(audio_file_id)
        if audio_file:
            audio_file.delete_from_db()
            message = 'Deleted {0} with id {1}'.format(audio_file_type, audio_file_id)
            return format_response(message, 200)
        message = '{0} with id {1} not found'.format(audio_file_type, audio_file_id)
        return format_response(message, 400)
