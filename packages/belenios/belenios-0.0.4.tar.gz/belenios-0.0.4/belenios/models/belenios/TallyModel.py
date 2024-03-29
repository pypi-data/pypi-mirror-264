from typing import List

from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.BallotModel import BallotModel
from belenios.models.belenios.EncryptedTallyRowModel import EncryptedTallyRowModel
from belenios.models.belenios.SizedEncryptedTallyModel import SizedEncryptedTallyModel


class TallyModel(BaseModel):
    ballots: Mapped[List[BallotModel]] = relationship('BallotModel', uselist=True, cascade="all, delete-orphan",
                                                      single_parent=True)
    election_bundle_id = Column(Integer, ForeignKey('election_bundle_model.id'), nullable=False, unique=True)
    election_bundle = relationship('ElectionBundleModel', back_populates='tally')
    encrypted_tally_rows: Mapped[List[EncryptedTallyRowModel]] = relationship("EncryptedTallyRowModel", uselist=True,
                                                                         cascade="all, delete-orphan",
                                                                         single_parent=True, back_populates="tally")
    sized_encrypted_tally_id = Column(Integer, ForeignKey('sized_encrypted_tally_model.id'), nullable=False)
    sized_encrypted_tally: Mapped[SizedEncryptedTallyModel] = relationship('SizedEncryptedTallyModel')

    def __str__(self):
        encrypted_tally_rows_info = ', '.join(
            str(encrypted_tally_row) for encrypted_tally_row in self.encrypted_tally_rows)

        return (
            f"TallyModel(\n"
            f"    ballots={self.ballots},\n"
            # f"    election_bundle_id={self.election_bundle_id},\n"
            # f"    election_bundle={self.election_bundle},\n"
            f"    encrypted_tally_rows=[{encrypted_tally_rows_info}],\n"
            f"    sized_encrypted_tally={self.sized_encrypted_tally}\n"
            f")"
        )
