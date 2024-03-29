from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.IType import IType
from belenios.custom_types.belenios.StringType import StringType
from belenios.models.BaseModel import BaseModel


class SaltModel(BaseModel):
    index = Column(IType, nullable=False)
    salt_value = Column(StringType, nullable=False)
    election_bundle_id = Column(Integer, ForeignKey('election_bundle_model.id'), nullable=False)
    election_bundle: Mapped['ElectionBundleModel'] = relationship("ElectionBundleModel", back_populates="salts")

    def to_json(self):
        return {
            'index': self.index,
            'salt_value': self.salt_value
        }

    def __str__(self):
        return (
            f"SaltModel(\n"
            f"    index={self.index},\n"
            f"    salt_value={self.salt_value},\n"
            # f"    election_bundle_id={self.election_bundle_id},\n"
            # f"    election_bundle={self.election_bundle}\n"
            f")"
        )