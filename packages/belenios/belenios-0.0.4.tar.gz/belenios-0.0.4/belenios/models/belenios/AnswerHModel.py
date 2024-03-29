from typing import List

from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.AnswerModel import AnswerModel
from belenios.models.belenios.CiphertextModel import CiphertextModel
from belenios.models.belenios.ProofModel import ProofModel
from belenios.utilities.Utility import Utility

assoc_answer_ciphertext= Table(
    "assoc_answer_ciphertext",
    BaseModel.metadata,
    Column("answer_id", Integer, ForeignKey("answer_model.id"), primary_key=True),
    Column("ciphertext_id", Integer, ForeignKey("ciphertext_model.id"), primary_key=True)
)

assoc_answer_i_proof = Table(
    "assoc_answer_i_proof",
    BaseModel.metadata,
    Column("answer_id", Integer, ForeignKey("answer_model.id"), primary_key=True),
    Column("i_proof_id", Integer, ForeignKey("i_proof_model.id"), primary_key=True)
)

class AnswerHModel(AnswerModel):
    id = Column(Integer, ForeignKey('answer_model.id'), primary_key=True)
    choices: Mapped[List[CiphertextModel]] = relationship('CiphertextModel', secondary=assoc_answer_ciphertext)
    individual_proofs = relationship('IProofModel', secondary=assoc_answer_i_proof)
    overall_proof_id: int = Column(Integer, ForeignKey('proof_model.id'), nullable=False)
    overall_proof: Mapped[ProofModel] = relationship('ProofModel', foreign_keys=[overall_proof_id])
    blank_proof1_id: int = Column(Integer, ForeignKey('proof_model.id'), nullable=True)
    blank_proof1: Mapped[ProofModel] = relationship('ProofModel', foreign_keys=[blank_proof1_id])
    blank_proof2_id: int = Column(Integer, ForeignKey('proof_model.id'), nullable=True)
    blank_proof2: Mapped[ProofModel] = relationship('ProofModel', foreign_keys=[blank_proof2_id])
    __mapper_args__ = {
        "polymorphic_identity": "AnswerHModel",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'AnswerHModel'

    def to_hash_sha256(self):
        delimiter = '|'
        data = (
                f"id={self.id}" + delimiter +
                f"choices={[choice.to_hash_sha256() for choice in self.choices]}" + delimiter +
                f"individual_proofs={[proof.to_hash_sha256() for proof in self.individual_proofs]}" + delimiter +
                f"overall_proof={self.overall_proof.to_hash_sha256()}" + delimiter +
                f"blank_proof1={self.blank_proof1.to_hash_sha256() if self.blank_proof1 else None}" + delimiter +
                f"blank_proof2={self.blank_proof2.to_hash_sha256() if self.blank_proof2 else None}"
        )
        sha256_hash = Utility.hash_sha256_as_hex(data.encode())
        return sha256_hash
    def __str__(self):
        choices_info = ', '.join(str(choice) for choice in self.choices)
        individual_proofs_info = ', '.join(str(individual_proof) for individual_proof in self.individual_proofs)
        return (
            f"AnswerHModel(\n"
            # f"    id={self.id},\n"
            f"    choices=[{choices_info}],\n"
            f"    individual_proofs=[{individual_proofs_info}],\n"
            # f"    overall_proof_id={self.overall_proof_id},\n"
            f"    overall_proof={self.overall_proof},\n"
            # f"    blank_proof1_id={self.blank_proof1_id},\n"
            f"    blank_proof1={self.blank_proof1},\n"
            # f"    blank_proof2_id={self.blank_proof2_id},\n"
            f"    blank_proof2={self.blank_proof2}\n"
            f")"
        )
