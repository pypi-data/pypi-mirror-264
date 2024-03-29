from sqlalchemy import Column

from belenios.custom_types.belenios.HType import HType
from belenios.custom_types.belenios.IType import IType
from belenios.models.BaseModel import BaseModel


class SizedEncryptedTallyModel(BaseModel):
    num_tallied = Column(IType, nullable=True)
    total_weight = Column(IType, nullable=True)
    encrypted_tally = Column(HType, nullable=True)

    def __str__(self):
        return (
            f"SizedEncryptedTallyModel(\n"
            f"    num_tallied={self.num_tallied},\n"
            f"    total_weight={self.total_weight},\n"
            f"    encrypted_tally={self.encrypted_tally}\n"
            f")"
        )