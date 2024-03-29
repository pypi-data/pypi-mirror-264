from abc import abstractmethod

from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey

from belenios.custom_types.belenios.StringType import StringType
from belenios.models.BaseModel import BaseModel


class AnswerModel(BaseModel):
    # __abstract__ = True
    type = Column(StringType, nullable=False)
    ballot_id = Column(Integer, ForeignKey('ballot_model.id'), nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "AnswerModel",
        "polymorphic_on": "type",
    }

    @abstractmethod
    def to_hash_sha256(self):
        pass
