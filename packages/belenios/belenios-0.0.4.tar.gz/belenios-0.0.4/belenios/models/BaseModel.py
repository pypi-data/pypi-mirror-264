import re

from sqlalchemy import Column, Integer, inspect
from sqlalchemy.orm import class_mapper
from sqlalchemy.orm import declarative_base

BaseModelDeclaration = declarative_base()


class BaseModel(BaseModelDeclaration):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    @classmethod
    def __init_subclass__(cls, **kwargs):
        # Convert class name to snake case and set it as __tablename__
        # cls.__tablename__ = cls.snake_case(cls.__name__).replace("_model", "")
        cls.__tablename__ = cls.snake_case(cls.__name__)
        super().__init_subclass__(**kwargs)

    @staticmethod
    def snake_case(name):
        name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
        return name

    def to_dict(self):
        result = {}

        # Iterate over columns from all parent classes
        for cls in self.__class__.__mro__:
            if hasattr(cls, '__table__'):
                for column in cls.__table__.columns:
                    result[column.name] = str(getattr(self, column.name))

        # Iterate over relationships from all parent classes
        for cls in self.__class__.__mro__:
            if hasattr(cls, '__mapper__'):
                for relationship in class_mapper(cls).relationships:
                    related_obj = getattr(self, relationship.key)
                    if related_obj is not None:
                        if relationship.uselist:
                            result[relationship.key] = [obj.to_dict() for obj in related_obj]
                        else:
                            result[relationship.key] = related_obj.to_dict()

        return result
    # def to_dict(self):
    #     result = {}
    #     for column in self.__table__.columns:
    #         result[column.name] = str(getattr(self, column.name))
    #     # Include polymorphic identity if present
    #     for relationship in class_mapper(self.__class__).relationships:
    #         related_obj = getattr(self, relationship.key)
    #         if related_obj is not None:
    #             if relationship.uselist:
    #                 result[relationship.key] = [obj.to_dict() for obj in related_obj]
    #             else:
    #                 result[relationship.key] = related_obj.to_dict()
    #     return result
    def __repr__(self):
        # return vars(self)
        field_strings = []
        for field, value in self._to_print_dict().items():
            field_strings.append(f'{field}={value}')
        return f"<{self.__class__.__name__} ({', '.join(field_strings)})>"

    def _to_print_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
