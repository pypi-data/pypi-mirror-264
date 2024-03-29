from typing import List

from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.ChannelMsgModel import ChannelMsgModel
from belenios.models.belenios.SignedMsgModel import SignedMsgModel

assoc_v_input_secret = Table(
    "assoc_v_input_secret",
    BaseModel.metadata,
    Column("v_input_id", Integer, ForeignKey("v_input_model.id"), primary_key=True),
    Column("secret_id", Integer, ForeignKey("channel_msg_model.id"), primary_key=True)
)
assoc_v_input_coefexps = Table(
    "assoc_v_input_coefexps",
    BaseModel.metadata,
    Column("v_input_id", Integer, ForeignKey("v_input_model.id"), primary_key=True),
    Column("coefexps_id", Integer, ForeignKey("signed_msg_model.id"), primary_key=True)
)
class VInputModel(BaseModel):
    polynomial_id = Column(Integer, ForeignKey('channel_msg_model.id'), nullable=False)
    polynomial: Mapped[ChannelMsgModel] = relationship('ChannelMsgModel', uselist=False, foreign_keys=[polynomial_id])
    secrets: Mapped[List[ChannelMsgModel]] = relationship('ChannelMsgModel', secondary=assoc_v_input_secret)
    coefexps: Mapped[List[SignedMsgModel]] = relationship('SignedMsgModel', secondary=assoc_v_input_coefexps)

    @staticmethod
    def load_from_json(dict):
        t = VInputModel(polynomial=ChannelMsgModel.load_from_json(dict["polynomial"]))
        t.secrets.extend([ChannelMsgModel.load_from_json(s) for s in dict["secrets"]])
        t.coefexps.extend([SignedMsgModel.load_from_json(s) for s in dict["coefexps"]])
        return t
