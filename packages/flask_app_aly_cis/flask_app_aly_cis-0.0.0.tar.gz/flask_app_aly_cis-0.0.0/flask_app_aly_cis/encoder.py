"""Custom JSON Encoder for the application."""

from connexion.apps.flask_app import FlaskJSONEncoder
from sqlalchemy.ext.declarative import DeclarativeMeta


class JSONEncoder(FlaskJSONEncoder):
    """
    Custom JSON Encoder class.

    This class extends FlaskJSONEncoder to provide custom JSON serialization.
    """

    include_nulls = False

    def default(self, o):
        """
        Convert custom objects to JSON serializable format.
        :param o: Object to be serialized
        :return: Serialized object
        """
        if isinstance(o.__class__, DeclarativeMeta) or hasattr(o, "to_dict"):
            # an SQLAlchemy class
            return o.to_dict()
        return FlaskJSONEncoder.default(self, o)
