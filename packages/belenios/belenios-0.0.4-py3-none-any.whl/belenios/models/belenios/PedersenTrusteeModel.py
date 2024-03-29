from typing import List

from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import event
from belenios.custom_types.belenios.ArrayOfIsType import ArrayOfIsType
from belenios.custom_types.belenios.IType import IType
from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.SignedMsgModel import SignedMsgModel
from belenios.models.belenios.TrusteeKindModel import TrusteeKindModel
from belenios.models.belenios.TrusteePublicKeyModel import TrusteePublicKeyModel
from belenios.utilities.command_line.DbSession import DbSession

assoc_pedersen_trustee_certs = Table(
    "assoc_pedersen_trustee_certs",
    BaseModel.metadata,
    Column("pedersen_trustee_id", Integer, ForeignKey("pedersen_trustee_model.id"), primary_key=True),
    Column("cert_id", Integer, ForeignKey("signed_msg_model.id"), primary_key=True)
)
assoc_pedersen_trustee_coefexps = Table(
    "assoc_pedersen_trustee_coefexps",
    BaseModel.metadata,
    Column("pedersen_trustee_id", Integer, ForeignKey("pedersen_trustee_model.id"), primary_key=True),
    Column("coefexp_id", Integer, ForeignKey("signed_msg_model.id"), primary_key=True)
)
assoc_pedersen_trustee_verification_keys = Table(
    "assoc_pedersen_trustee_verification_keys",
    BaseModel.metadata,
    Column("pedersen_trustee_id", Integer, ForeignKey("pedersen_trustee_model.id"), primary_key=True),
    Column("verification_key_id", Integer, ForeignKey("trustee_public_key_model.id"), primary_key=True)
)


class PedersenTrusteeModel(TrusteeKindModel):
    id = Column(Integer, ForeignKey('trustee_kind_model.id'), primary_key=True)
    threshold = Column(IType, nullable=False)
    trustee_ids: Mapped[List[IType]] = Column(ArrayOfIsType, nullable=False)
    certs: Mapped[List[SignedMsgModel]] = relationship('SignedMsgModel', uselist=True,
                                                       secondary=assoc_pedersen_trustee_certs)
    coefexps: Mapped[List[SignedMsgModel]] = relationship('SignedMsgModel', uselist=True,
                                                          secondary=assoc_pedersen_trustee_coefexps)
    verification_keys: Mapped[List[TrusteePublicKeyModel]] = relationship('TrusteePublicKeyModel', uselist=True,
                                                                          secondary=assoc_pedersen_trustee_verification_keys)

    __mapper_args__ = {
        "polymorphic_identity": "PedersenTrusteeModel"
    }

    def __init__(self, *args, **kwargs):
        trustee_ids = kwargs.pop('trustee_ids', None)
        super().__init__(*args, **kwargs)
        self.trustee_kind_type = 'PedersenTrusteeModel'
        self.trustee_ids = trustee_ids if trustee_ids is not None else []

    def append_trustee_id(self, trustee_id):
        if trustee_id not in self.trustee_ids:
            a = [i for i in self.trustee_ids]
            a.append(trustee_id)
            self.trustee_ids = a
