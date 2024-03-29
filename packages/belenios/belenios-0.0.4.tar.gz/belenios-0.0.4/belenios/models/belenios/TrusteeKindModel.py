from sqlalchemy import Column, Integer, ForeignKey

from belenios.custom_types.belenios.StringType import StringType
from belenios.models.BaseModel import BaseModel


class TrusteeKindModel(BaseModel):
    election_bundle_id = Column(Integer, ForeignKey('election_bundle_model.id'), nullable=False)
    trustee_kind_type = Column(StringType, nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "TrusteeKindModel",
        "polymorphic_on": trustee_kind_type
    }

    def __str__(self):
        return (
            f"TrusteeKindModel(\n"
            # f"    election_bundle_id={self.election_bundle_id},\n"
            f"    trustee_kind_type={self.trustee_kind_type}\n"
            f")"
        )