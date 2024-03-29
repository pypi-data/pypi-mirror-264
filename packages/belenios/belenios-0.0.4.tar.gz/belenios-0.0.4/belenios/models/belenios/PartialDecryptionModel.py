from typing import List

from belenios.models.belenios.DecryptionProofRowModel import DecryptionProofRowModel
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.DecryptionFactorRowModel import DecryptionFactorRowModel


class PartialDecryptionModel(BaseModel):
    decryption_factor_rows: Mapped[List[DecryptionFactorRowModel]] = relationship("DecryptionFactorRowModel",
                                                                                  uselist=True,
                                                                                  cascade="all, delete-orphan",
                                                                                  single_parent=True)
    decryption_proofs_rows: Mapped[List[DecryptionProofRowModel]] = relationship("DecryptionProofRowModel",
                                                                                 uselist=True,
                                                                                 cascade="all, delete-orphan",
                                                                                 single_parent=True)
