from Crypto.Util.number import inverse
from sqlalchemy.orm.exc import NoResultFound

from belenios.custom_types.belenios.EventType import EventType
from belenios.dataclass.dataclass import EncryptedText
from belenios.models.belenios.CiphertextModel import CiphertextModel
from belenios.models.belenios.CredentialModel import CredentialModel
from belenios.models.belenios.EncryptedTallyRowModel import EncryptedTallyRowModel
from belenios.models.belenios.PedersenTrusteeModel import PedersenTrusteeModel
from belenios.models.belenios.ResultModel import ResultModel
from belenios.models.belenios.ResultRowModel import ResultRowModel
from belenios.models.belenios.SingleTrusteeModel import SingleTrusteeModel
from belenios.models.belenios.TallyModel import TallyModel
from belenios.models.belenios.VoterModel import VoterModel
from belenios.utilities.ElGamal import ElGamal
from belenios.utilities.TrusteesKeysProtocol import TrusteesKeysProtocol
from belenios.utilities.Utility import Utility
from belenios.utilities.command_line.DbSession import DbSession


class ServerCore:
    @staticmethod
    def make_election_unique(election):
        election.uuid = Utility.generate_base58_string(14)
        DbSession().session.commit()

    @staticmethod
    def check_voters_credentials_and_salts(election_uuid, public_credentials, salts):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return False
        election = election_bundle.election
        if election is None:
            return False
        salts_seen = []
        public_credential_seen = []
        for index, pc in public_credentials.items():
            try:
                existing_voter = DbSession().session.query(VoterModel).filter_by(email=pc["email"]).first()
            except NoResultFound:
                return False
            if str(pc["index"]) != str(index):
                return False
            if pc["weight"] != existing_voter.weight:
                return False
            if pc["public_credential"] in public_credential_seen:
                return False
            if salts[pc["index"]] in salts_seen:
                return False
            salts_seen.append(salts[pc["index"]])
            public_credential_seen.append(pc["public_credential"])

        if len(public_credential_seen) != len(election_bundle.voters) or len(salts_seen) != len(election_bundle.voters):
            return False
        return True

    @staticmethod
    def import_public_key_single_trustee(election_uuid, trustee_public_key, trustee_id):
        single_trustee = SingleTrusteeModel()
        single_trustee.trustee_id = trustee_id
        single_trustee.trustee_public_key = trustee_public_key
        print(trustee_public_key)
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        # ServerAdministratorCore().add_single_trustees(self.app.pargs.uuid, int(self.app.pargs.count))

        # 2. S checks γ
        # We can check is the key and the pok is correctly generated :
        if TrusteesKeysProtocol().check_proof_trustee_public_key(election_bundle.election,
                                                                 single_trustee.trustee_public_key):
            print("Trustee key is valid")
        else:
            print("Trustee key is invalid")
            return False

        election_bundle.trustee_kinds.append(single_trustee)
        DbSession().session.commit()
        return single_trustee

    @staticmethod
    def import_cert_pedersen_trustee(election_uuid, signed_msg, trustee_id):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        pedersen_trustee = None
        for pedersen_trustee_iter in election_bundle.trustee_kinds:
            if pedersen_trustee_iter.trustee_kind_type == "PedersenTrusteeModel":
                pedersen_trustee = pedersen_trustee_iter
                break
        if pedersen_trustee is None:
            pedersen_trustee = PedersenTrusteeModel()
            pedersen_trustee.threshold = 2
            election_bundle.trustee_kinds.append(pedersen_trustee)
        pedersen_trustee.append_trustee_id(trustee_id)

        # ServerAdministratorCore().add_single_trustees(self.app.pargs.uuid, int(self.app.pargs.count))

        # 2. S checks γ
        # We can check is the cert and the signed_msg is correctly generated :
        if Utility.check_signed_msg(signed_msg, signed_msg.signed_object.verification, election_bundle.election):
            print("Trustee cert is valid")
        else:
            print("Trustee cert is invalid")
            return False

        pedersen_trustee.certs.append(signed_msg)
        # print(pedersen_trustee)
        # print(trustee_kind_row)
        # print(trustee_kind_row.trustee_kinds)
        DbSession().session.commit()
        return pedersen_trustee

    @staticmethod
    def import_coefexps_verification_keys_pedersen_trustee(election_uuid, v_output):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        pedersen_trustee = None
        for pedersen_trustee_iter in election_bundle.trustee_kinds:
            if pedersen_trustee_iter.trustee_kind_type == "PedersenTrusteeModel":
                pedersen_trustee = pedersen_trustee_iter
                break
        if pedersen_trustee is None:
            pedersen_trustee = PedersenTrusteeModel()
            pedersen_trustee.threshold = 2
            election_bundle.trustee_kinds.append(pedersen_trustee)

        if len(election_bundle.polynomials) > len(pedersen_trustee.coefexps):
            pedersen_trustee.coefexps = []
            for p_i in election_bundle.polynomials:
                pedersen_trustee.coefexps.append(p_i.coefexps)
        pedersen_trustee.verification_keys.append(v_output.trustee_public_key)
        DbSession().session.commit()
        return pedersen_trustee

    @staticmethod
    def compute_election_public_key(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        # 10. S creates the election E
        election_bundle.election.public_key = TrusteesKeysProtocol().compute_election_public_key(election_bundle)
        print("Election public key is %s" % election_bundle.election.public_key)
        DbSession().session.commit()

        return election_bundle

    @staticmethod
    def add_questions(election_uuid, questions):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        for question in questions:
            election_bundle.election.questions.append(question)
        DbSession().session.commit()

        return questions

    @staticmethod
    def make_election_immutable(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None

        # Fix ElectionModel, trustee_kinds, public_credentials and publish the bundle to avoid later manipulation and
        election_bundle.setup_data.election = election_bundle.election.to_hash_sha256()
        print("Election hash is %s" % election_bundle.setup_data.election)

        DbSession().session.commit()
        return election_bundle

    @staticmethod
    def print_election_bundle(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        print(election_bundle)

    @staticmethod
    def add_to_tally(election_uuid, ballot_to_add):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None

        tally = DbSession().session.query(TallyModel).filter_by(election_bundle=election_bundle).first()
        if tally is None:
            print("Tally invalid")
            return None

        replaced = False
        for index, ballot in enumerate(tally.ballots):
            if ballot.credential == ballot_to_add.credential:
                tally.ballots[index] = ballot_to_add
                replaced = True
                break
        if not replaced:
            tally.ballots.append(ballot_to_add)
        DbSession().session.commit()
        return tally

    @staticmethod
    def compute_encrypted_tally(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        election = election_bundle.election
        tally = DbSession().session.query(TallyModel).filter_by(election_bundle=election_bundle).first()
        if tally is None:
            print("Tally invalid")
            return None

        for index_question, question in enumerate(election.questions):
            encrypted_tally_row = EncryptedTallyRowModel()
            is_blank = question.type == "QuestionHModel" and question.blank
            for index_answer in range(len(question.answers) + int(is_blank)):  # loop over choices + blank
                if question.type == 'QuestionHModel':
                    # Initialize the product of ciphertexts for this answer
                    product_ciphertext = [1, 1]

                    # Iterate over each ballot
                    for ballot in election_bundle.tally.ballots:
                        answer = ballot.answers[index_question]
                        choice = answer.choices[index_answer]
                        credential = DbSession().session.query(CredentialModel).filter_by(
                            public_credential=ballot.credential).first()
                        if credential is None:
                            print("Credential not found.")
                            return None
                        weight = credential.weight
                        # Multiply the corresponding ciphertext to the power of weight
                        product_ciphertext[0] *= (choice.alpha ** weight)
                        product_ciphertext[1] *= (choice.beta ** weight)
                        product_ciphertext[0] %= election.group.p
                        product_ciphertext[1] %= election.group.p
                        # ciphertext_answer = answer[index]
                        # product_ciphertext = (
                        #     product_ciphertext[0] * ciphertext_answer[0],
                        #     product_ciphertext[1] * ciphertext_answer[1])

                    # Append the resulting ciphertext to the array
                    ciphertext = CiphertextModel()
                    ciphertext.alpha = product_ciphertext[0]
                    ciphertext.beta = product_ciphertext[1]
                    encrypted_tally_row.ciphertexts.append(ciphertext)
                else:
                    print("not implemented")
                    return None
                    # # Initialize the array of ciphertexts for this answer
                    # answer_ciphertexts = []
                    #
                    # # Iterate over each ballot
                    # for ballot in ballots:
                    #     answer = ballot.answers[index]
                    #     weight = ballot.weight
                    #
                    #     # Ensure weight is 1 for non-homomorphic questions
                    #     if weight != 1:
                    #         raise ValueError("Non-homomorphic question has weight other than 1")
                    #
                    #     # Append the corresponding ciphertext
                    #     ciphertext_answer = answer[index]
                    #     answer_ciphertexts.append(ciphertext_answer)
                    #
                    # # Append the array of ciphertexts to the array
                    # ciphertexts_question.append(answer_ciphertexts)

            # Append the array of ciphertexts for this question to the encrypted tally array
            election_bundle.tally.encrypted_tally_rows.append(encrypted_tally_row)
        tally.sized_encrypted_tally.num_tallied = len(election_bundle.tally.ballots)

        tally.sized_encrypted_tally.total_weight = 0
        for ballot in election_bundle.tally.ballots:
            credential = DbSession().session.query(CredentialModel).filter_by(
                public_credential=ballot.credential).first()
            if credential is None:
                print("Credential not found.")
                return None
            tally.sized_encrypted_tally.total_weight += credential.weight
        # TODO: hash the tally
        # tally.sized_encrypted_tally.encrypted_tally  =
        DbSession().session.commit()
        return tally

    @staticmethod
    def set_event_encrypted_tally(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        event = Utility.put_new_event(election_bundle)
        event.type = EventType.EncryptedTally
        DbSession().session.commit()
        return event

    @staticmethod
    def add_event_partial_decryption(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        event = Utility.put_new_event(election_bundle)
        event.type = EventType.PartialDecryption
        DbSession().session.commit()
        return event

    @staticmethod
    def lambda_factor(trustee_ids, delta, group):
        l = 1
        for trustee_id in trustee_ids:
            if trustee_id == delta:
                continue
            # print("j", inverse(trustee_id - delta, group.q))
            l *= trustee_id * inverse(trustee_id - delta, group.q)
        return l % group.q

    @staticmethod
    def compute_result(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        trustees_number = 0
        for trustee_kind in election_bundle.trustee_kinds:
            if trustee_kind.trustee_kind_type == "SingleTrusteeModel":
                trustees_number += 1
            else:
                trustees_number += len(trustee_kind.trustee_ids)
                # TODO: handle correctly group of trustees

        if len(election_bundle.owned_partial_decryptions) < trustees_number:
            print("Not enough partial decryption")
            return None
        group = election_bundle.election.group
        # g = election_bundle.election.group.g
        # q = election_bundle.election.group.q
        # total_weight = election_bundle.tally.sized_encrypted_tally.total_weight
        result = ResultModel()
        for i, question in enumerate(election_bundle.election.questions):
            result_row = ResultRowModel()
            is_blank = question.type == "QuestionHModel" and question.blank
            for j in range(len(question.answers) + int(is_blank)):
                F_ij = 1
                for owned_partial_decryption in election_bundle.owned_partial_decryptions:
                    trustee_kind = Utility.get_trustee_kind_from_id(owned_partial_decryption.trustee_id,
                                                                    election_bundle)
                    partial_decryption = owned_partial_decryption.partial_decryption
                    if trustee_kind.trustee_kind_type == "SingleTrusteeModel":
                        F_ijt = partial_decryption.decryption_factor_rows[i].decryption_factors[j]
                    else:
                        lambda_delta_I = ServerCore.lambda_factor(trustee_kind.trustee_ids,
                                                                  owned_partial_decryption.trustee_id, group)
                        F_ijt = pow(partial_decryption.decryption_factor_rows[i].decryption_factors[j], lambda_delta_I,
                                    group.p)
                    F_ij *= F_ijt

                aij = election_bundle.tally.encrypted_tally_rows[i].ciphertexts[j]
                alpha_aij = aij.alpha
                beta_aij = aij.beta
                a = EncryptedText([(alpha_aij, beta_aij)])

                res_ij = ElGamal().decrypt_from_int(a, private_key=None, group=group, exponential=True, right=F_ij,
                                                    max_dlp=10 ** 5)

                # m_prime = (beta_aij * inverse(F_ij, q)) % q
                # print("jjj", beta_aij * F_ij)
                # teta = beta_aij / F_ij
                # teta = (beta_aij * inverse(F_ij, q)) % q
                # res_ij = ElGamal().discrete_logarithm(teta, g, total_weight*10)
                # print("res_ij",res_ij)
                # res_ij = ElGamal().discrete_logarithm(teta, g, q)
                result_row.result_cells.append(res_ij)
            result.result_rows.append(result_row)
        election_bundle.result = result
        DbSession().session.commit()
        return result

    @staticmethod
    def set_event_result(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        event = Utility.put_new_event(election_bundle)
        event.type = EventType.Result
        DbSession().session.commit()
        return event

    @staticmethod
    def get_array_of_result(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None

        result = []

        for i, result_row in enumerate(election_bundle.result.result_rows):
            row = []
            for j, result_cell in enumerate(result_row.result_cells):
                row.append(result_cell)
            result.append(row)

        return result
