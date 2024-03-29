from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.IType import IType
from belenios.custom_types.belenios.StringType import StringType
from belenios.models.BaseModel import BaseModel


class CredentialModel(BaseModel):
    index = Column(IType, nullable=False)
    public_credential = Column(StringType, nullable=False)
    weight = Column(IType, nullable=True)
    email = Column(StringType, nullable=False)
    election_bundle_id = Column(Integer, ForeignKey('election_bundle_model.id'), nullable=False)
    election_bundle: Mapped['ElectionBundleModel'] = relationship("ElectionBundleModel",
                                                                  back_populates="public_credentials")

    def to_json(self):
        return {
            'index': self.index,
            'public_credential': self.public_credential,
            'weight': self.weight,
            'email': self.email
        }
    def __str__(self):
        return (
            f"CredentialModel(\n"
            f"    index={self.index},\n"
            f"    public_credential={self.public_credential},\n"
            f"    weight={self.weight},\n"
            f"    email={self.email},\n"
            # f"    election_bundle_id={self.election_bundle_id},\n"
            # f"    election_bundle={self.election_bundle}\n"
            f")"
        )