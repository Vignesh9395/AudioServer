"""
Author: Venkata Vignesh B

Description: Resource Class for Podcast
"""
from flask_restful import reqparse

from utilities.validator import string_check
from utilities.validator import list_check
from utilities.validator import integer_check


class Podcast:
    """
    Parser for Podcast Metadata
    """

    parser = reqparse.RequestParser()
    parser.add_argument('id',
                        type=integer_check(),
                        required=True,
                        help="Podcast id of type integer is required!",
                        ignore=False
                        )
    parser.add_argument('name',
                        type=string_check(100),
                        required=True,
                        location='json',
                        help="Podcast name of type string upto 100 characters is required!"
                        )
    parser.add_argument('duration',
                        type=integer_check(),
                        required=True,
                        help="Podcast Duration of type integer is required!"
                        )
    parser.add_argument('host',
                        type=string_check(100),
                        required=True,
                        location='json',
                        help="Podcast Host of type string upto 100 characters is required!"
                        )
    parser.add_argument('participants',
                        type=string_check(100),
                        required=False,
                        action='append',
                        location='json',
                        help="Podcast Participant name of type string upto 100 "
                             "characters is required!"
                        )
    parser.add_argument('participants',
                        type=list_check(10),
                        required=False,
                        location='json',
                        help="Podcast Participants should be a list of max 10 participants!"
                        )