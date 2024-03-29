from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey, Table
from sqlalchemy.orm import relationship

from belenios.models.BaseModel import BaseModel
from belenios.utilities.Utility import Utility

assoc_i_proof_and_proofs = Table(
    "assoc_i_proof_and_proofs",
    BaseModel.metadata,
    Column("i_proof_model_id", ForeignKey("i_proof_model.id"), primary_key=True),
    Column("proof_model_id", ForeignKey("proof_model.id"), primary_key=True),
)


class IProofModel(BaseModel):
    i_proof_model_id = Column(Integer, ForeignKey('i_proof_model.id'))
    proofs = relationship("ProofModel", secondary=assoc_i_proof_and_proofs)

    def to_hash_sha256(self):
        delimiter = '|'
        data = (
                f"id={self.id}" + delimiter +
                f"proofs={[proof.to_hash_sha256() for proof in self.proofs]}" + delimiter
        )
        sha256_hash = Utility.hash_sha256_as_hex(data.encode())
        return sha256_hash
