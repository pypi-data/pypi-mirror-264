from sqlalchemy import Column

from belenios.custom_types.belenios.ZqType import ZqType
from belenios.models.BaseModel import BaseModel
from belenios.utilities.Utility import Utility


class ProofModel(BaseModel):
    challenge = Column(ZqType, nullable=False)
    response = Column(ZqType, nullable=False)

    def to_hash_sha256(self):
        delimiter = '|'
        data = (
                f"id={self.id}" + delimiter +
                f"challenge={self.challenge}" + delimiter +
                f"response={self.response}"
        )
        sha256_hash = Utility.hash_sha256_as_hex(data.encode())
        return sha256_hash

    def to_json(self):
        return {
            "challenge": self.challenge,
            "response": self.response
        }

    def __str__(self):
        return (
            f"ProofModel(\n"
            f"    challenge={self.challenge},\n"
            f"    response={self.response}\n"
            f")"
        )

    @staticmethod
    def load_from_json(dict):
        return ProofModel(challenge=int(dict['challenge']), response=int(dict['response']))
