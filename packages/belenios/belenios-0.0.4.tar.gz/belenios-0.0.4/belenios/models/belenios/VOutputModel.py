from typing import List

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.ChannelMsgModel import ChannelMsgModel
from belenios.models.belenios.SignedMsgModel import SignedMsgModel


from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.ChannelMsgModel import ChannelMsgModel
from belenios.models.belenios.SignedMsgModel import SignedMsgModel
from belenios.models.belenios.TrusteePublicKeyModel import TrusteePublicKeyModel


class VOutputModel(BaseModel):
    private_key_id = Column(Integer, ForeignKey('channel_msg_model.id'), nullable=False)
    private_key: Mapped[ChannelMsgModel] = relationship('ChannelMsgModel', uselist=False)
    trustee_public_key_id: int = Column(Integer, ForeignKey('trustee_public_key_model.id'), nullable=False)
    trustee_public_key: Mapped[TrusteePublicKeyModel] = relationship('TrusteePublicKeyModel', uselist=False)