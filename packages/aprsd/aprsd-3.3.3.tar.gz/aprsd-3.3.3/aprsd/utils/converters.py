from datafiles import converters
from datetime import datetime


class MyDateTime(converters.Converter, datetime):

    @classmethod
    def to_preserialization_data(cls, python_value, **kwargs):
        # Convert `datetime` to a value that can be serialized
        return python_value.isoformat()

    @classmethod
    def to_python_value(cls, deserialized_data, **kwargs):
        # Convert file value back into a `datetime` object
        return datetime.fromisoformat(deserialized_data)
