from belenios.models.belenios.DecryptionFactorRowModel import DecryptionFactorRowModel
from belenios.models.belenios.OwnedPartialDecryptionModel import OwnedPartialDecryptionModel
from belenios.models.belenios.PartialDecryptionModel import PartialDecryptionModel
from belenios.utilities.TrusteesKeysProtocol import TrusteesKeysProtocol
from belenios.utilities.Utility import Utility
from belenios.utilities.command_line.DbSession import DbSession


class TrusteeCore:

    @staticmethod
    def generates_single_trustee_public_key(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        return TrusteesKeysProtocol().generate_single_trustee_key(election_bundle.election)

    @staticmethod
    def generates_perdersen_trustee_keys(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        return TrusteesKeysProtocol().generate_perdersen_trustee_keys(election_bundle.election)

    @staticmethod
    def generates_perdersen_trustee_polynomial(election_uuid, threshold, seed, trustee_id):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        return TrusteesKeysProtocol().generate_perdersen_trustee_polynomial(election_bundle, threshold, seed,
                                                                            trustee_id)
    @staticmethod
    def generates_perdersen_trustee_vinput(election_uuid, seed, trustee_id):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        return TrusteesKeysProtocol().generate_perdersen_trustee_vinput(election_bundle, seed,trustee_id)

    @staticmethod
    def check_perdersen_trustee_vinput(election_uuid, seed, trustee_id, vinput):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        return TrusteesKeysProtocol().check_perdersen_trustee_vinput(election_bundle, seed, trustee_id, vinput)

    @staticmethod
    def generates_perdersen_trustee_voutput(election_uuid, seed, trustee_id, v_input):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        return TrusteesKeysProtocol().generate_perdersen_trustee_voutput(election_bundle, seed, trustee_id,
                                                                         v_input)

    @staticmethod
    def partial_decrypt_encrypted_ballot(election_uuid, private_key, trustee_id):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None

        owned_partial_decryption = OwnedPartialDecryptionModel()
        owned_partial_decryption.trustee_id = trustee_id
        owned_partial_decryption.partial_decryption = PartialDecryptionModel()

        p = election_bundle.election.group.p
        for encrypted_tally_row in election_bundle.tally.encrypted_tally_rows:
            # print("dd")
            decryption_factor_row = DecryptionFactorRowModel()
            # print("dd", encrypted_tally_row)
            # print("dd", encrypted_tally_row.ciphertexts)

            for ciphertext in encrypted_tally_row.ciphertexts:
                # TODO: check mod q or g  and -1
                decryption_factor = pow(ciphertext.alpha, -1 * private_key, p)
                # a = EncryptedText([(ciphertext.alpha, ciphertext.beta)])
                # print("test", ElGamal().decrypt_from_int(a, private_key ,election_bundle.election.group, True, decryption_factor))
                decryption_factor_row.decryption_factors.append(decryption_factor)
            #     TODO: make decryption_proof_row
            owned_partial_decryption.partial_decryption.decryption_factor_rows.append(decryption_factor_row)
        election_bundle.owned_partial_decryptions.append(owned_partial_decryption)
        DbSession().session.commit()
        return owned_partial_decryption
