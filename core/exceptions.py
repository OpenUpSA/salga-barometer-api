from rest_framework.exceptions import APIException


class TooManyResultsException(APIException):
    status_code = 400
    default_detail = 'Too Many Results'
    default_code = 'too_many_results'
