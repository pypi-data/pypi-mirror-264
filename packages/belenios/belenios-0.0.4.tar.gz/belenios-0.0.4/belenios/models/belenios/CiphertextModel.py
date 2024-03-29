from sqlalchemy import Column

from belenios.custom_types.belenios.GType import GType
from belenios.models.BaseModel import BaseModel
from belenios.utilities.Utility import Utility


class CiphertextModel(BaseModel):
    alpha = Column(GType, nullable=False)
    beta = Column(GType, nullable=False)

    def to_hash_sha256(self):
        delimiter = '|'
        data = (
                f"alpha={self.alpha}" + delimiter +
                f"beta={self.beta}" + delimiter
        )
        sha256_hash = Utility.hash_sha256_as_hex(data.encode())
        return sha256_hash

    def __str__(self):
        return (
            f"CiphertextModel(\n"
            f"    alpha={self.alpha},\n"
            f"    beta={self.beta}\n"
            f")"
        )