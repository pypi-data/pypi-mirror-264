from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.models.belenios.AnswerModel import AnswerModel
from belenios.utilities.Utility import Utility


class AnswerNhModel(AnswerModel):
    id = Column(Integer, ForeignKey('answer_model.id'), primary_key=True)
    choices: Mapped["CiphertextModel"] = relationship('CiphertextModel', uselist=False)
    choices_id: int = Column(Integer, ForeignKey('ciphertext_model.id'), nullable=False)
    proof_id: int = Column(Integer, ForeignKey('proof_model.id'), nullable=False)
    proof: Mapped['ProofModel'] = relationship('ProofModel')
    __mapper_args__ = {
        "polymorphic_identity": "AnswerNhModel",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = 'AnswerNhModel'

    def __str__(self):
        return (
            f"AnswerNhModel(id={self.id}, "
            f"choices_id={self.choices_id}, "
            f"choices={self.choices}, "
            f"proof_id={self.proof_id},"
            f"proof={self.proof})"
        )

    def to_hash_sha256(self):
        delimiter = '|'
        data = (
                f"id={self.id}" + delimiter +
                f"choices={self.choice.to_hash_sha256() }" + delimiter +
                f"individual_proofs={[proof.to_hash_sha256() for proof in self.individual_proofs]}" + delimiter +
                f"proof={self.proof.to_hash_sha256()}"
        )
        sha256_hash = Utility.hash_sha256_as_hex(data.encode())
        return sha256_hash
