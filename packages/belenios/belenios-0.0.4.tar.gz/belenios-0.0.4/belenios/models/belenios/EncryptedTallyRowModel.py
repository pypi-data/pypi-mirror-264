from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel

assoc_encrypted_tally_row_and_ciphertext = Table(
    "assoc_encrypted_tally_row_and_ciphertext",
    BaseModel.metadata,
    Column("encrypted_tally_row_model_id", ForeignKey("encrypted_tally_row_model.id"), primary_key=True),
    Column("ciphertext_model_id", ForeignKey("ciphertext_model.id"), primary_key=True),
)


class EncryptedTallyRowModel(BaseModel):
    tally_id = Column(Integer, ForeignKey('tally_model.id'))
    tally: Mapped['TallyModel'] = relationship('TallyModel')
    ciphertexts = relationship("CiphertextModel", secondary=assoc_encrypted_tally_row_and_ciphertext)
