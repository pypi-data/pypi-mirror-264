from sqlalchemy.types import TypeDecorator, Boolean


class BType(TypeDecorator):
    impl = Boolean
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = bool(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = bool(value)
        return value

    def process_literal_param(self, value, dialect):
        return value
