"""
Author: Venkata Vignesh B

Description: Resource Class for Song
"""
from flask_restful import reqparse
from utilities.validator import string_check
from utilities.validator import integer_check


class Song:
    """
        Parser for Song Metadata
        """

    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=integer_check(),
                        required=True,
                        help="Song id of type integer is required!",
                        ignore=False
                        )
    parser.add_argument('name',
                        type=string_check(100),
                        required=True,
                        location='json',
                        help="Song name of type string upto 100 characters is required!"
                        )
    parser.add_argument('duration',
                        type=integer_check(),
                        required=True,
                        help="Song Duration of type integer is required!"
                        )