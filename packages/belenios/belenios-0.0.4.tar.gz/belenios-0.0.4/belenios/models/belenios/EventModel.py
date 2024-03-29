from sqlalchemy import Column, Integer, Enum, ForeignKey

from belenios.custom_types.belenios.HType import HType
from belenios.custom_types.belenios.IType import IType
from belenios.models.BaseModel import BaseModel
from belenios.custom_types.belenios.EventType import EventType


class EventModel(BaseModel):
    election_bundle_id: int = Column(Integer, ForeignKey('election_bundle_model.id'), nullable=False)
    parent = Column(HType, nullable=True)
    height = Column(IType, nullable=False)
    type = Column(Enum(EventType), nullable=False)
    payload = Column(HType, nullable=True)

    def __str__(self):
        return (
            f"EventModel(\n"
            # f"    election_bundle_id={self.election_bundle_id},\n"
            f"    parent={self.parent},\n"
            f"    height={self.height},\n"
            f"    type={self.type},\n"
            f"    payload={self.payload}\n"
            f")"
        )