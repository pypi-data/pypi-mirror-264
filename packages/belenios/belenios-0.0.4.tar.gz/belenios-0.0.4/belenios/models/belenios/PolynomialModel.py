from typing import List

from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.ChannelMsgModel import ChannelMsgModel
from belenios.models.belenios.SignedMsgModel import SignedMsgModel

assoc_polynomial_secret = Table(
    "assoc_polynomial_secret",
    BaseModel.metadata,
    Column("polynomial_id", Integer, ForeignKey("polynomial_model.id"), primary_key=True),
    Column("secret_id", Integer, ForeignKey("channel_msg_model.id"), primary_key=True)
)
class PolynomialModel(BaseModel):
    election_bundle_id = Column(Integer, ForeignKey('election_bundle_model.id'), nullable=False)
    trustee_id = Column(Integer, nullable=False)
    polynomial_id = Column(Integer, ForeignKey('channel_msg_model.id'), nullable=False)
    polynomial: Mapped[ChannelMsgModel] = relationship('ChannelMsgModel', uselist=False, foreign_keys=[polynomial_id])
    secrets: Mapped[List[ChannelMsgModel]] = relationship('ChannelMsgModel', secondary=assoc_polynomial_secret)
    coefexps_id = Column(Integer, ForeignKey('signed_msg_model.id'), nullable=False)
    coefexps: Mapped[SignedMsgModel] = relationship('SignedMsgModel', uselist=False)
