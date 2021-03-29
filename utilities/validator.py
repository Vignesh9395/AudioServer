"""
Author: Venkata Vignesh B

Description: Field Parser for Custom Rules on input fields
"""


class ValidationError(Exception):
    pass


def string_check(max_length):
    """
    Method to check if input is string and is of 100 characters max
    """
    def validate(input_data):
        assert type(input_data) == str
        if len(input_data) <= max_length:
            return input_data
        raise ValidationError("failed to satisfy max length of {}".format(max_length))
    return validate


def list_check(max_length):
    """
        Method to check if input is List and is of length 10 max
        """
    def validate(input_data):
        assert type(input_data) == list
        if len(input_data) <= max_length:
            return input_data
        raise ValidationError("failed to satisfy max length of {}".format(max_length))
    return validate


def integer_check():
    """
        Method to check if input is Integer
        """
    def validate(input_data):
        assert type(input_data) == int
        return input_data
    return validate
