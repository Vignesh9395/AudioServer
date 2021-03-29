"""
Author: Venkata Vignesh B

Description: Resource Class for Audiobook
"""
from flask_restful import reqparse

from utilities.validator import string_check
from utilities.validator import integer_check


class Audiobook:
    """
        Parser for Audiobook Metadata
        """

    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=integer_check(),
                        required=True,
                        help="Audiobook id of type integer is required!",
                        ignore=False
                        )
    parser.add_argument('title',
                        type=string_check(100),
                        required=True,
                        location='json',
                        help="Audiobook title of type string upto 100 characters is required!"
                        )
    parser.add_argument('duration',
                        type=integer_check(),
                        required=True,
                        help="Audiobook Duration of type integer is required!"
                        )
    parser.add_argument('author',
                        type=string_check(100),
                        required=True,
                        location='json',
                        help="Audiobook author of type string upto 100 characters is required!"
                        )
    parser.add_argument('narrator',
                        type=string_check(100),
                        required=True,
                        location='json',
                        help="Audiobook narrator of type string upto 100 characters is required!"
                        )