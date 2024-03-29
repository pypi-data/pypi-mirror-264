from sqlalchemy import Column, Integer

from belenios.custom_types.belenios.IType import IType
from belenios.models.BaseModel import BaseModel


class HeaderModel(BaseModel):
    version = Column(IType, nullable=False)
    timestamp = Column(IType, nullable=False)
