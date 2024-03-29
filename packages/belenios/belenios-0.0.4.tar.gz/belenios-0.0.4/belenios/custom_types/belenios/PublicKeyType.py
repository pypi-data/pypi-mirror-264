from sqlalchemy.types import TypeDecorator

from belenios.custom_types.belenios.GType import GType


class PublicKeyType(TypeDecorator):
    impl = GType

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        return value

    def process_literal_param(self, value, dialect):
        return value
