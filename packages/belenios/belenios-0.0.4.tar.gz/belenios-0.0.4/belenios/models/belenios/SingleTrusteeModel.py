from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.IType import IType
from belenios.models.belenios.TrusteeKindModel import TrusteeKindModel


class SingleTrusteeModel(TrusteeKindModel):
    id = Column(Integer, ForeignKey('trustee_kind_model.id'), primary_key=True)
    trustee_id = Column(IType, nullable=False)
    trustee_public_key_id: int = Column(Integer, ForeignKey('trustee_public_key_model.id'), nullable=False)
    trustee_public_key: Mapped['TrusteePublicKeyModel'] = relationship('TrusteePublicKeyModel')
    __mapper_args__ = {
        "polymorphic_identity": "SingleTrusteeModel"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trustee_kind_type = 'SingleTrusteeModel'
