from sqlalchemy.types import TypeDecorator, VARCHAR


class HType(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            # Ensure value is a string and convert it to lowercase
            value = str(value).lower()
            # Validate hash length (SHA256 produces 64-character hashes)
            if len(value) != 64:
                raise ValueError("Hash value must be 64 characters long")
        return value

    def process_result_value(self, value, dialect):
        return value

    def process_literal_param(self, value, dialect):
        return value
