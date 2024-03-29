from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel

assoc_decryption_proof_row_and_ciphertext = Table(
    "assoc_decryption_proof_row_and_ciphertext",
    BaseModel.metadata,
    Column("decryption_proof_row_model_id", ForeignKey("decryption_proof_row_model.id"), primary_key=True),
    Column("proof_model_id", ForeignKey("proof_model.id"), primary_key=True),
)


class DecryptionProofRowModel(BaseModel):
    partial_decryption_model_id = Column(Integer, ForeignKey('partial_decryption_model.id'))
    proofs = relationship("ProofModel", secondary=assoc_decryption_proof_row_and_ciphertext)
