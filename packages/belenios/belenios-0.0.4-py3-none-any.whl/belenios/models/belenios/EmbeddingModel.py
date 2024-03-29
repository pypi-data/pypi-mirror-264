from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.IType import IType
from belenios.models.BaseModel import BaseModel


class EmbeddingModel(BaseModel):
    padding = Column(IType, nullable=False)
    bits_per_int = Column(IType, nullable=False)
    group_id: int = Column(Integer, ForeignKey('group_model.id'), nullable=False)
    group: Mapped['GroupModel'] = relationship('GroupModel', back_populates='embedding')

    def __str__(self):
        return (
            f"EmbeddingModel(\n"
            f"    padding={self.padding},\n"
            f"    bits_per_int={self.bits_per_int},\n"
            # f"    group_id={self.group_id},\n"
            # f"    group={self.group}\n"
            f")"
        )