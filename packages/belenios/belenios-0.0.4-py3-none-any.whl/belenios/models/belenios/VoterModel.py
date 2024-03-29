from typing import List

from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.IType import IType
from belenios.custom_types.belenios.StringType import StringType
from belenios.models.BaseModel import BaseModel

# note for a Core table, we use the sqlalchemy.Column construct,
# not sqlalchemy.orm.mapped_column
assoc_elections_bundle_and_voters = Table(
    "assoc_elections_bundle_and_voters",
    BaseModel.metadata,
    Column("election_bundle_model_id", ForeignKey("election_bundle_model.id"), primary_key=True),
    Column("voter_model_id", ForeignKey("voter_model.id"), primary_key=True),
)


class VoterModel(BaseModel):
    email = Column(StringType, nullable=False, unique=True)
    weight = Column(IType, nullable=False)
    election_bundles: Mapped[List['ElectionBundleModel']] = relationship(secondary=assoc_elections_bundle_and_voters,
                                                                         back_populates="voters")
    def __str__(self):
        return (
            f"VoterModel(\n"
            f"    email={self.email},\n"
            f"    weight={self.weight},\n"
            # f"    election_bundles={self.election_bundles}\n"
            f")"
        )