import json

from sqlalchemy.types import TypeDecorator, VARCHAR


class ArrayOfIsType(TypeDecorator):
    impl = VARCHAR
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            # Serialize the array of ints to strings JSON
            if not isinstance(value, list):
                value = [value]
            for i, v in enumerate(value):
                value[i] = int(v)
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            # Deserialize the JSON to an array of ints
            value = [int(v) for v in json.loads(value)]
        return value

    def process_literal_param(self, value, dialect):
        return value
