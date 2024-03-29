from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.IType import IType
from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.PartialDecryptionModel import PartialDecryptionModel
from belenios.models.belenios.TrusteeKindModel import TrusteeKindModel


class OwnedPartialDecryptionModel(BaseModel):
    election_bundle_id: int = Column(Integer, ForeignKey('election_bundle_model.id'), nullable=False)
    trustee_id = Column(IType, nullable=False)
    partial_decryption: Mapped[PartialDecryptionModel] = relationship('PartialDecryptionModel',
                                                                      uselist=False)  # payload : H
    partial_decryption_id = Column(Integer, ForeignKey('partial_decryption_model.id'))

    def __str__(self):
        return (
            f"OwnedPartialDecryptionModel(\n"
            # f"    election_bundle_id={self.election_bundle_id},\n"
            f"    trustee_id={self.trustee_id},\n"
            f"    trustee_kind={self.trustee_kind},\n"
            f"    partial_decryption={self.partial_decryption},\n"
            # f"    partial_decryption_id={self.partial_decryption_id}\n"
            f")"
        )
