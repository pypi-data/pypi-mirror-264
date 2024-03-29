from enum import Enum


class RoleType(Enum):
    ServerAdministrator = 'ServerAdministrator'
    CredentialAuthority = 'CredentialAuthority'
    Trustee = 'Trustee'
    Voter = 'Voter'
    VotingServer = 'VotingServer'
