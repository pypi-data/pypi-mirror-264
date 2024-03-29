from sqlalchemy import Column

from belenios.custom_types.belenios.StringType import StringType
from belenios.models.BaseModel import BaseModel


class EncryptedDataModel(BaseModel):
    ciphertext = Column(StringType, nullable=False)
    tag = Column(StringType, nullable=False)
    iv = Column(StringType, nullable=False)

    @staticmethod
    def load_from_json(dict):
        return EncryptedDataModel(ciphertext=dict["ciphertext"], tag=dict["tag"], iv=dict["iv"])
