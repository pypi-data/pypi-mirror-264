from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.StringType import StringType
from belenios.custom_types.belenios.ArrayOfStringsType import ArrayOfStringsType
from belenios.models.BaseModel import BaseModel
from belenios.utilities.Utility import Utility


class QuestionModel(BaseModel):
    # __abstract__ = True
    type = Column(StringType, nullable=False)
    question = Column(StringType, nullable=True)
    answers = Column(ArrayOfStringsType, nullable=True)
    extra = Column(StringType, nullable=True)
    election_id: int = Column(Integer, ForeignKey('election_model.id'), nullable=False)
    election: Mapped['ElectionModel'] = relationship('ElectionModel', back_populates='questions')
    __mapper_args__ = {
        "polymorphic_identity": "QuestionModel",
        "polymorphic_on": "type",
    }
    def to_hash_sha256(self):
        delimiter = '|'
        data = (
                f"type={self.type}" + delimiter +
                f"question={self.question}" + delimiter +
                f"answers={self.answers}" + delimiter +
                f"extra={self.extra}" + delimiter
        )
        sha256_hash = Utility.hash_sha256_as_hex(data.encode())
        return sha256_hash

    def __str__(self):
        return (
            f"QuestionModel(\n"
            f"    type={self.type},\n"
            f"    question={self.question},\n"
            f"    answers={self.answers},\n"
            f"    extra={self.extra}\n"
            f")"
        )