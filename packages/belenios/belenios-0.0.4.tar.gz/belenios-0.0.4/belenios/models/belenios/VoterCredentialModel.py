from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, Mapped

from belenios.models.BaseModel import BaseModel


class VoterCredentialModel(BaseModel):
    election_id = Column(Integer, ForeignKey('election_model.id'), nullable=False)
    election: Mapped['ElectionModel'] = relationship("ElectionModel")
    voter_id = Column(Integer, ForeignKey('voter_model.id'), nullable=False)
    voter: Mapped['VoterModel'] = relationship("VoterModel")
    credential_id = Column(Integer, ForeignKey('credential_model.id'), nullable=False)
    credential: Mapped['CredentialModel'] = relationship("CredentialModel")
