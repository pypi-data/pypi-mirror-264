from sqlalchemy.types import TypeDecorator, Integer


class IType(TypeDecorator):
    impl = Integer
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = int(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = int(value)
        return value

    def process_literal_param(self, value, dialect):
        return value
