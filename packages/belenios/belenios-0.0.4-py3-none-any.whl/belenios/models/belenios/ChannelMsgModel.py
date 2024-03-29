from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.GType import GType
from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.EncryptedMsgModel import EncryptedMsgModel


class ChannelMsgModel(BaseModel):
    recipient = Column(GType, nullable=False)
    message_id = Column(Integer, ForeignKey('encrypted_msg_model.id'), nullable=False)
    message: Mapped[EncryptedMsgModel] = relationship('EncryptedMsgModel', uselist=False)
    @staticmethod
    def load_from_json( dict):
        return ChannelMsgModel(recipient=dict['recipient'], message=EncryptedMsgModel.load_from_json(dict['message']))
