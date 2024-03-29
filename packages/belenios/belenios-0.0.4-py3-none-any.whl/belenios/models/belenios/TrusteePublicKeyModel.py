from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from belenios.custom_types.belenios.PublicKeyType import PublicKeyType
from belenios.models.BaseModel import BaseModel


class TrusteePublicKeyModel(BaseModel):
    proof_id = Column(Integer, ForeignKey('proof_model.id'), nullable=False)
    pok = relationship('ProofModel')
    public_key = Column(PublicKeyType, nullable=False)

    def to_json(self):
        return {
            "proof_id": self.proof_id,
            "public_key": self.public_key,
            "pok": self.pok.to_json() if self.pok else None
        }