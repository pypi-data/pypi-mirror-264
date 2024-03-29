from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from belenios.custom_types.belenios.StringType import StringType
from belenios.models.BaseModel import BaseModel


class SignatureModel(BaseModel):
    ballot_id = Column(Integer, ForeignKey('ballot_model.id'), nullable=False)
    hash = Column(StringType, nullable=False)
    proof_id = Column(Integer, ForeignKey('proof_model.id'), nullable=False)
    proof = relationship('ProofModel')
