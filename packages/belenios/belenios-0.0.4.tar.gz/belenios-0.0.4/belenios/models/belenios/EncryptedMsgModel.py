from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.GType import GType
from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.EncryptedDataModel import EncryptedDataModel


class EncryptedMsgModel(BaseModel):
    alpha = Column(GType, nullable=False)
    beta = Column(GType, nullable=False)
    data_id = Column(Integer, ForeignKey('encrypted_data_model.id'), nullable=False)
    data: Mapped[EncryptedDataModel] = relationship('EncryptedDataModel', uselist=False)

    @staticmethod
    def load_from_json(dict):
        return EncryptedMsgModel(alpha=int(dict["alpha"]), beta=int(dict["beta"]), data=EncryptedDataModel.load_from_json(dict["data"]))
