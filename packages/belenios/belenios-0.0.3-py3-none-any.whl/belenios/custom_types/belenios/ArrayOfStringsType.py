import json

from sqlalchemy.types import TypeDecorator, VARCHAR


class ArrayOfStringsType(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            # Serialize the array of strings to JSON
            if not isinstance(value, list):
                value = [value]
            for i,v in enumerate(value):
                value[i] = str(v)
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            # Deserialize the JSON to an array of strings
            value = json.loads(value)
        return value

    def process_literal_param(self, value, dialect):
        return value
