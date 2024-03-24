"""This module handle api exception."""


class ApiError(Exception):
    """
    api base exception
    """

    status_code = 500

    def __init__(self, message: str, details=None, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        self.details = details
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
