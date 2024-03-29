from dataclasses import asdict

from Crypto.Random import random

from belenios.dataclass.dataclass import PrivateCredential
from belenios.models.belenios.CredentialModel import CredentialModel
from belenios.models.belenios.SaltModel import SaltModel
from belenios.models.belenios.VoterModel import VoterModel
from belenios.utilities.Utility import Utility
from belenios.utilities.command_line.DbSession import DbSession


class CredentialAuthorityCore:

    @staticmethod
    def generate_secret_credential(index_already_used):
        # Generate random prefix of 14 characters from Base58 alphabet
        prefix = Utility.generate_base58_string(14)

        # Generate random index NNNN
        index = random.randint(0, 9999)
        for i in range(10000):
            if index in index_already_used:
                index = random.randint(0, 9999)
            else:
                break

        # Construct secret credential in the form XXX-XXXX-XXX-XXXX-NNNN
        c = f"{prefix[:3]}-{prefix[3:7]}-{prefix[7:10]}-{prefix[10:14]}-{index:04}"
        return c, prefix, index

    @staticmethod
    def generate_voters_credentials_and_salts(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None, None
        private_credentials = {}
        public_credentials = {}
        salts = {}
        index_already_used = []
        for i, voter in enumerate(election_bundle.voters):
            c, prefix, index = CredentialAuthorityCore.generate_secret_credential(index_already_used)
            private_credential = PrivateCredential(index, c, voter.email)

            index_already_used.append(index)

            s = Utility.generate_base58_string(22)
            for i in range(10000):
                if index in index_already_used:
                    s = Utility.generate_base58_string(22)
                else:
                    break
            salt = SaltModel()
            salt.index = index
            salt.salt_value = s
            salt.election_bundle = election_bundle
            DbSession().session.add(salt)

            x = Utility.derive_secret_exponent(prefix, salt, election_bundle.election)
            public_key = pow(election_bundle.election.group.g, x,
                             election_bundle.election.group.p)  # Calculate g^x mod p

            credential = CredentialModel()
            credential.index = index
            credential.public_credential = public_key
            credential.weight = voter.weight
            credential.email= voter.email
            credential.election = election_bundle.election
            election_bundle.public_credentials.append(credential)

            # voter_credential = VoterCredentialModel()
            # voter_credential.election = election_bundle.election
            # voter_credential.voter = voter
            # voter_credential.credential = credential
            # DbSession().session.add(voter_credential)


            DbSession().session.commit()

            private_credentials[index] = asdict(private_credential)
            public_credentials[index] = credential.to_json()
            salts[index] = salt.to_json()

        return private_credentials, public_credentials, salts

    @staticmethod
    def format_output_voters_credentials_and_salts(credentials, salts):
        pass

    @staticmethod
    def send_to_voters_their_credentials(app, election_bundle, private_credentials):
        for voter_credential_id, c in private_credentials.items():
            voter = DbSession().session.query(VoterModel).filter_by(id=voter_credential_id).first()

            print("Sending mail to voter: %s" % (voter.email))
            Utility.send_mail(app, election_bundle.election.credential_authority, voter.email,
                              "You're credential is : %s" % c)
