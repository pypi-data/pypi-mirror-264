"""This module handles custom exceptions."""

import logging
import traceback
from typing import Union

from connexion.exceptions import ConnexionException
from tenacity import RetryError
from werkzeug.exceptions import HTTPException

from flask import jsonify
from flask_app_aly_cis.core.exception import ApiError


def generate_error_message(message, status_code, error_id=""):
    """

    :param message:
    :param status_code:
    :param error_id:
    :return:
    """
    error_dict = {
        'error': {
            "message": message,
            "code": status_code,
            "details": [
                {
                    "error_id": f"ERROR-{error_id or status_code}"
                }
            ]
        }
    }
    return error_dict


def exception_handler(error: Union[RetryError, ApiError, ConnexionException, HTTPException, Exception]):
    """

    :param error:
    :return:
    """
    details = ""
    if isinstance(error, RetryError):
        message = str(error.last_attempt)
        status_code = 500
    elif isinstance(error, ApiError):
        status_code = error.status_code
        message = error.message
        details = error.details
    elif isinstance(error, ConnexionException):
        status_code = error.status
        message = error.details
    elif isinstance(error, HTTPException):
        status_code = error.code or 500
        message = str(error.description)
    else:
        status_code = 500
        message = f"Unexpected exception. ({error})"

    if not details:
        details = message
    logging.getLogger().debug(''.join(traceback.format_tb(error.__traceback__)))
    error_dict = generate_error_message(message, status_code)
    logging.getLogger().error({**error_dict, "details": details})
    if status_code == 500:
        traceback.print_exc()
    response = jsonify(error_dict)
    response.status_code = status_code
    return response
