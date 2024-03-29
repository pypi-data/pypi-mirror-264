from sqlalchemy.types import TypeDecorator, VARCHAR


class UuidType(TypeDecorator):
    impl = VARCHAR
    cache_ok = True
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if len(value) < 14:
            raise ValueError("Value must be at least 14 characters long")
        for letter in value:
            if letter not in "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz":
                raise ValueError("Value must be base58 encoded")
        return value

    def process_result_value(self, value, dialect):
        return value

    def process_literal_param(self, value, dialect):
        return value
