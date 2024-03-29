from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.GType import GType
from belenios.custom_types.belenios.NType import NType
from belenios.custom_types.belenios.StringType import StringType
from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.EmbeddingModel import EmbeddingModel
from belenios.utilities.Utility import Utility


class GroupModel(BaseModel):
    description = Column(StringType, nullable=False)
    g = Column(GType, nullable=False)
    p = Column(NType, nullable=False)
    q = Column(NType, nullable=False)
    election_id: int = Column(Integer, ForeignKey('election_model.id'), nullable=False)
    election: Mapped['ElectionModel'] = relationship('ElectionModel', back_populates='group')
    embedding: Mapped["EmbeddingModel"] = relationship('EmbeddingModel', back_populates='group',
                                                       uselist=False, cascade="all, delete-orphan",
                                                       single_parent=True)
    def to_hash_sha256(self):
        delimiter = '|'
        data = (
                f"description={self.description}" + delimiter +
                f"g={self.g}" + delimiter +
                f"p={self.p}" + delimiter +
                f"q={self.q}"
            # Add embedding if needed
        )
        sha256_hash = Utility.hash_sha256_as_hex(data.encode())
        return sha256_hash

    def __str__(self):
        return (
            f"GroupModel(\n"
            f"    description={self.description},\n"
            f"    g={self.g},\n"
            f"    p={self.p},\n"
            f"    q={self.q},\n"
            # f"    election_id={self.election_id},\n"
            # f"    election={self.election},\n"
            f"    embedding={self.embedding}\n"
            f")"
        )