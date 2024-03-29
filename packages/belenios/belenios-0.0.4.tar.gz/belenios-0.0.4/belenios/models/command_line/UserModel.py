from sqlalchemy import Column, Enum

from belenios.custom_types.belenios.StringType import StringType
from belenios.custom_types.command_line.RoleType import RoleType
from belenios.models.BaseModel import BaseModel


class UserModel(BaseModel):
    username = Column(StringType, nullable=False)
    password_hash = Column(StringType, nullable=False)
    role = Column(Enum(RoleType), nullable=False)
