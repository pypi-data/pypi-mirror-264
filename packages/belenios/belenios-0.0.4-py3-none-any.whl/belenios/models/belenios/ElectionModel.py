from typing import List

from sqlalchemy import Column
from sqlalchemy.orm import relationship, Mapped

from belenios.custom_types.belenios.IType import IType
from belenios.custom_types.belenios.PublicKeyType import PublicKeyType
from belenios.custom_types.belenios.StringType import StringType
from belenios.custom_types.belenios.UuidType import UuidType
from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.GroupModel import GroupModel
from belenios.models.belenios.QuestionModel import QuestionModel
from belenios.utilities.Utility import Utility


class ElectionModel(BaseModel):
    version = Column(IType, nullable=False)
    description = Column(StringType, nullable=False)
    name = Column(StringType, nullable=False)
    group: Mapped[GroupModel] = relationship('GroupModel', back_populates='election',
                                                            uselist=False, cascade="all, delete-orphan",
                                                            single_parent=True)
    public_key = Column(PublicKeyType, nullable=True)
    questions: Mapped[List["QuestionModel"]] = relationship('QuestionModel', back_populates='election',
                                                            uselist=True, cascade="all, delete-orphan",
                                                            single_parent=True)
    uuid = Column(UuidType, nullable=True)
    administrator = Column(StringType, nullable=True)
    credential_authority = Column(StringType, nullable=True)
    election_bundle: Mapped["ElectionBundleModel"] = relationship('ElectionBundleModel')
    def to_hash_sha256(self):
        delimiter = '|'
        data = (
                f"version={self.version}" + delimiter +
                f"description={self.description}" + delimiter +
                f"name={self.name}" + delimiter +
                f"group={self.group.to_hash_sha256()}" + delimiter +
                f"public_key={self.public_key}" + delimiter +
                f"questions={[question.to_hash_sha256() for question in self.questions]}" + delimiter +
                f"uuid={self.uuid}" + delimiter +
                f"administrator={self.administrator}" + delimiter +
                f"credential_authority={self.credential_authority}"
        )
        sha256_hash = Utility.hash_sha256_as_hex(data.encode())
        return sha256_hash

    def __str__(self):
        return (
            f"ElectionModel(\n"
            f"    version={self.version},\n"
            f"    description={self.description},\n"
            f"    name={self.name},\n"
            f"    group={self.group},\n"
            f"    public_key={self.public_key},\n"
            f"    questions={[str(question) for question in self.questions]},\n"
            f"    uuid={self.uuid},\n"
            f"    administrator={self.administrator},\n"
            f"    credential_authority={self.credential_authority},\n"
            # f"    election_bundle={self.election_bundle}\n"
            f")"
        )