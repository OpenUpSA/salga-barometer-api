from rest_framework.exceptions import APIException


class TooManyResultsException(APIException):
    status_code = 400
    default_detail = 'Too Many Results'
    default_code = 'too_many_results'


class NotEnoughParameters(APIException):
    """
    Show when not all query parameters have been set.
    """
    status_code = 400
    default_detail = 'Not Enough Parameters'
    default_code = 'not_enough_parameters'
