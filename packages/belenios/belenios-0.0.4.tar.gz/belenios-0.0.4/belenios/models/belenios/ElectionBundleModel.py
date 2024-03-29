from typing import List

from sqlalchemy import Column
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel
from belenios.models.belenios.CredentialModel import CredentialModel
from belenios.models.belenios.EventModel import EventModel
from belenios.models.belenios.OwnedPartialDecryptionModel import OwnedPartialDecryptionModel
from belenios.models.belenios.PolynomialModel import PolynomialModel
from belenios.models.belenios.ResultModel import ResultModel
from belenios.models.belenios.SaltModel import SaltModel
from belenios.models.belenios.TallyModel import TallyModel
from belenios.models.belenios.TrusteeKindModel import TrusteeKindModel
from belenios.models.belenios.VoterModel import VoterModel, assoc_elections_bundle_and_voters


class ElectionBundleModel(BaseModel):
    election_id = Column(Integer, ForeignKey('election_model.id'), nullable=False)
    election = relationship('ElectionModel', back_populates='election_bundle')
    trustee_kinds: Mapped[List[TrusteeKindModel]] = relationship('TrusteeKindModel', uselist=True,
                                                                     cascade="all, delete-orphan", single_parent=True)
    voters: Mapped[List[VoterModel]] = relationship(secondary=assoc_elections_bundle_and_voters,
                                                    back_populates="election_bundles")
    public_credentials: Mapped[List[CredentialModel]] = relationship('CredentialModel', uselist=True)
    salts: Mapped[List[SaltModel]] = relationship('SaltModel', uselist=True)
    setup_data_id = Column(Integer, ForeignKey('setup_data_model.id'), nullable=False)
    setup_data = relationship('SetupDataModel')
    events: Mapped[List[EventModel]] = relationship('EventModel', uselist=True, cascade="all, delete-orphan",
                                                      single_parent=True)
    tally: Mapped[TallyModel] = relationship('TallyModel')
    owned_partial_decryptions: Mapped[List[OwnedPartialDecryptionModel]] = relationship('OwnedPartialDecryptionModel',
                                                                                          uselist=True,
                                                                                          cascade="all, delete-orphan",
                                                                                          single_parent=True)
    result_id: int = Column(Integer, ForeignKey('result_model.id'), nullable=True)
    result: Mapped[ResultModel] = relationship('ResultModel', uselist=False)
    polynomials: Mapped[List[PolynomialModel]] = relationship('PolynomialModel', uselist=True,
                                                              cascade="all, delete-orphan", single_parent=True)

    def __str__(self):
        trustee_kinds_info = ', '.join(str(trustee_kind) for trustee_kind in self.trustee_kinds)
        voters_info = ', '.join(str(voter) for voter in self.voters)
        public_credentials_info = ', '.join(str(credential) for credential in self.public_credentials)
        salts_info = ', '.join(str(salt) for salt in self.salts)
        events_info = ', '.join(str(event) for event in self.events)
        owned_partial_decryptions_info = ', '.join(
            str(owned_partial_decryption) for owned_partial_decryption in self.owned_partial_decryptions)

        return (
            f"ElectionBundleModel(\n"
            f"    election={self.election},\n"
            f"    trustee_kinds=[{trustee_kinds_info}],\n"
            f"    voters=[{voters_info}],\n"
            f"    public_credentials=[{public_credentials_info}],\n"
            f"    salts=[{salts_info}],\n"
            f"    setup_data={self.setup_data},\n"
            f"    events=[{events_info}],\n"
            f"    tally={self.tally},\n"
            f"    owned_partial_decryptions=[{owned_partial_decryptions_info}],\n"
            f"    result={self.result}\n"
            f")"
        )