from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.ProofModel import ProofModel
from belenios.models.belenios.SignedObjectModel import SignedObjectModel


class SignedMsgModel(BaseModel):
    signed_object_id = Column(Integer, ForeignKey('signed_object_model.id'), nullable=False)
    signed_object: Mapped[SignedObjectModel] = relationship('SignedObjectModel', uselist=False)
    signature_id = Column(Integer, ForeignKey('proof_model.id'), nullable=False)
    signature: Mapped[ProofModel] = relationship('ProofModel', uselist=False)

    # def to_json(self):
    #     return {
    #         'signed_object': self.signed_object.to_json(),
    #         'signature': self.signature.to_json(),
    #     }

    @staticmethod
    def load_from_json(dict):
        return SignedMsgModel(signed_object=SignedObjectModel.load_from_json(dict['signed_object']),
                              signature=ProofModel.load_from_json(dict['signature']))
