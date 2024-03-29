from typing import List

from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.GType import GType
from belenios.custom_types.belenios.StringType import StringType
from belenios.custom_types.belenios.UuidType import UuidType
from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.AnswerModel import AnswerModel
from belenios.models.belenios.SignatureModel import SignatureModel
from belenios.utilities.Utility import Utility


class BallotModel(BaseModel):
    tally_id = Column(Integer, ForeignKey('tally_model.id'), nullable=True)
    election_uuid = Column(UuidType, nullable=True)
    election_hash = Column(StringType, nullable=False)
    credential = Column(GType, nullable=False)  # A ballot references in its credential member the public \n
    # credential S = gsecret(c,s) (c being the secret credential, s being the associated salt) of the voter
    answers: Mapped[List[AnswerModel]] = relationship('AnswerModel', uselist=True, cascade="all, delete-orphan",
                                                         single_parent=True)
    # TODO: add credential_id
    signature: Mapped[SignatureModel] = relationship('SignatureModel', uselist=False, single_parent=True)
    # TODO: change to_hash_sha256 to respect To compute the hash used in signatures, the ballot without the signature
    #  field is first serialized as a JSON compact string, where object fields are ordered as specified in this document
    def to_hash_sha256(self):
        delimiter = '|'
        data = (
                f"election_uuid={self.election_uuid}" + delimiter +
                f"election_hash={self.election_hash}" + delimiter +
                f"credential={self.credential}" + delimiter +
                f"answers={[answer.to_hash_sha256() for answer in self.answers]}" + delimiter +
                f"signature=EXCLUDED"  # The signature needs a credential c and uses the hash of the surrounding
            # ballot (without the signature field)
        )
        sha256_hash = Utility.hash_sha256_as_hex(data.encode())
        return sha256_hash
    def __str__(self):
        answers_info = ', '.join(str(answer) for answer in self.answers)
        return (
            f"BallotModel(\n"
            f"    election_uuid={self.election_uuid},\n"
            f"    election_hash={self.election_hash},\n"
            f"    credential={self.credential},\n"
            f"    answers=[{answers_info}],\n"
            f"    signature={self.signature}\n"
            f")"
        )