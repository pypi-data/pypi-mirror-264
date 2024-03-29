from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.ArrayOfGsType import ArrayOfGsType
from belenios.models.BaseModel import BaseModel


class DecryptionFactorRowModel(BaseModel):
    partial_decryption_id = Column(Integer, ForeignKey('partial_decryption_model.id'))
    decryption_factors = Column(ArrayOfGsType, nullable=False)

    def __init__(self, *args, **kwargs):
        if 'decryption_factors' not in kwargs:
            kwargs['decryption_factors'] = []
        super().__init__(*args, **kwargs)