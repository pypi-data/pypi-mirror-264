"""Entry point for the application."""

import logging

import connexion
from connexion import FlaskApp
from flask_cors import CORS
from flask_request_id_header.middleware import RequestID
from requests import Response
from werkzeug.exceptions import default_exceptions

from flask import Flask, redirect, request
from flask_app_aly_cis import encoder, settings
from flask_app_aly_cis.core.exception_handler import exception_handler

SWAGGER_FILES = [
    {"base_path": "/api", "file": "swagger.yaml"},
    {"base_path": "/api/v1", "file": "swagger.yaml"},
]


def setup_connexion_routes(connexion_app: connexion.App):
    """
    Setup routes for Connexion application.

    :param connexion_app: Connexion application object
    """
    for swagger in SWAGGER_FILES:
        connexion_app.add_api(swagger.get('file'), base_path=swagger.get('base_path'), validate_responses=True,
                              arguments={"CONFIG": getattr(settings, 'swagger_config', {'title': "flask app"})},
                              pythonic_params=True)


def setup_flask_routes(flask_app: Flask):
    """
    Setup routes for Flask application.

    :param flask_app: Flask application object
    """
    @flask_app.route("/")
    @flask_app.route("/documentation")
    @flask_app.route("/documentation/")
    @flask_app.route("/api")
    @flask_app.route("/api/")
    @flask_app.route("/api/v1")
    @flask_app.route("/api/v1/")
    def documentation_root():
        return redirect("/api/documentation/")

    @flask_app.before_request
    def before_request_func():
        if request.path not in settings.PATH_TO_NOT_LOGGED:
            logging.getLogger().info("Begin Request")
            # ElasticSearchController().log_request_infor(logging.getLogger().request_info())

    @flask_app.after_request
    def after_request_func(response: Response):
        if request.path not in settings.PATH_TO_NOT_LOGGED:
            print('response: ', response)
            logging.getLogger().info(response.json)
            # ElasticSearchController().log_request_infor(logging.getLogger().request_info())
        return response


def setup_configuration(flask_app: Flask):
    """
    Setup configuration for Flask application.

    :param flask_app: Flask application object
    """
    try:
        flask_app.config.from_object("flask_app_aly_cis.settings")
    except ImportError as error:
        logging.getLogger().error(error)
        raise


def setup_exception_handlers(flask_app: FlaskApp):
    """
    Setup exception handlers for Flask application.

    :param flask_app: Flask application object
    """
    for exception in default_exceptions:
        flask_app.app.register_error_handler(exception, exception_handler)

    flask_app.add_error_handler(Exception, exception_handler)


def main():
    """
    Main function to initialize and run the application.
    """
    app = connexion.App(__name__, specification_dir='./swagger/', options={"swagger_url": "documentation"})
    app.app.json_encoder = encoder.JSONEncoder
    setup_connexion_routes(app)
    setup_configuration(app.app)
    setup_exception_handlers(app)
    setup_flask_routes(app.app)
    RequestID(app.app)
    CORS(app=app.app)
    # SecretsController()
    return app


if __name__ == "__main__":
    main().run()
