from abc import abstractmethod

from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey

from belenios.custom_types.belenios.StringType import StringType
from belenios.models.BaseModel import BaseModel


class SignedObjectModel(BaseModel):
    # __abstract__ = True
    type = Column(StringType, nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "SignedObject",
        "polymorphic_on": "type",
    }

    @abstractmethod
    def to_hash_sha256(self):
        pass

    @staticmethod
    def load_from_json(dict):
        if dict['type'] == "RawCoefexpsModel":
            from belenios.models.belenios.RawCoefexpsModel import RawCoefexpsModel
            return RawCoefexpsModel.load_from_json(dict)
        elif dict['type'] == "SignedStringModel":
            from belenios.models.belenios.SignedStringModel import SignedStringModel
            return SignedStringModel.load_from_json(dict)
        else:
            print("Type not implemented", dict['type'])
            return None
