from Crypto.Util.number import inverse

from belenios.models.belenios.AnswerHModel import AnswerHModel
from belenios.models.belenios.AnswerNhModel import AnswerNhModel
from belenios.models.belenios.CiphertextModel import CiphertextModel
from belenios.models.belenios.IProofModel import IProofModel
from belenios.models.belenios.ProofModel import ProofModel
from belenios.utilities.ElGamal import ElGamal
from belenios.utilities.ProofOfKnowledge import ProofOfKnowledge
from belenios.utilities.Utility import Utility


class AnswerUtility:
    @staticmethod
    def gen_S0(election_bundle, secret_c):
        return election_bundle.setup_data.election + "|" + str(
            pow(election_bundle.election.group.g, secret_c, election_bundle.election.group.q))

    @staticmethod
    def gen_S(election_bundle, secret_c, ciphertext_model_arr, ):
        a = [str(c.alpha) + "," + str(c.beta) for c in ciphertext_model_arr]
        b = ','.join(a)
        return AnswerUtility.gen_S0(election_bundle, secret_c) + '|' + b

    @staticmethod
    def compute_iprove(election, S, choices_for_a_question, encrypted_text_and_k, id_answer, answer):
        encryption = answer.choices[id_answer]
        alpha = encrypted_text_and_k.chunk[0][0]
        beta = encrypted_text_and_k.chunk[0][1]
        k = encrypted_text_and_k.chunk[0][2]
        proofs = []
        Ajs = []
        Bjs = []
        sum_challenge = 0
        # 1. for j ̸= i:
        for j, choice in enumerate(choices_for_a_question):
            if j == id_answer:
                continue
            pi_proof = ProofModel()
            pi_proof.challenge = Utility.generate_number_in_q(election.group)
            pi_proof.response = Utility.generate_number_in_q(election.group)
            proofs.append(pi_proof)
            sum_challenge += pi_proof.challenge
            Aj = (pow(election.group.g, pi_proof.response, election.group.p) * pow(alpha, pi_proof.challenge,
                                                                                   election.group.p)) % election.group.p
            Ajs.append(Aj)
            inv_g_Mi = inverse(pow(election.group.g, choice, election.group.p), election.group.p)
            beta_factor = (beta * inv_g_Mi) % election.group.p
            Bj = (pow(election.public_key, pi_proof.response, election.group.p) * pow(beta_factor, pi_proof.challenge,
                                                                                      election.group.p)) % election.group.p
            Bjs.append(Bj)
        # 2. πi is created as follows:
        # we generate A = g^w using a key pair, where private_key = A and public_key = w
        tmp = Utility.gen_key_el_gamal(election.group)
        w = tmp.private_key
        Ai = tmp.public_key

        Ajs.insert(id_answer, Ai)
        Bj = pow(election.public_key, w, election.group.p)
        Bjs.insert(id_answer, Bj)

        hash = ProofOfKnowledge.Hiprove(S, encryption, Ajs, Bjs)
        pi_proof = ProofModel()
        pi_proof.challenge = hash - (sum_challenge % election.group.q)
        pi_proof.response = (w - k * pi_proof.challenge) % election.group.q
        proofs.insert(id_answer, pi_proof)
        iproof = IProofModel()
        iproof.proofs = proofs
        return iproof

    @staticmethod
    def check_iprove(election, S, choices_for_a_question, id_answer, id_choice, answer):
        pi_proofs = answer.individual_proofs[id_choice].proofs
        encryption = answer.choices[id_choice]
        alpha = encryption.alpha
        beta = encryption.beta
        Ajs = []
        Bjs = []
        sum_challenge = 0
        # 1. for j ̸= i:
        for j, (choice, pi_proof) in enumerate(zip(choices_for_a_question, pi_proofs)):
            sum_challenge += pi_proof.challenge
            Aj = (pow(election.group.g, pi_proof.response, election.group.p) * pow(alpha, pi_proof.challenge,
                                                                                   election.group.p)) % election.group.p
            Ajs.append(Aj)
            inv_g_Mi = inverse(pow(election.group.g, choice, election.group.p), election.group.p)
            beta_factor = (beta * inv_g_Mi) % election.group.p
            Bj = (pow(election.public_key, pi_proof.response, election.group.p) * pow(beta_factor, pi_proof.challenge,
                                                                                      election.group.p)) % election.group.p
            Bjs.append(Bj)

        hash = ProofOfKnowledge.Hiprove(S, encryption, Ajs, Bjs)
        sum_challenge -= pi_proofs[id_choice].challenge
        sum_challenge %= election.group.q
        return hash == sum_challenge

    @staticmethod
    def compute_individuals_proofs(election_bundle, secret, answer, choices_for_a_question, encrypted_text_and_k_arr):
        S = AnswerUtility.gen_S(election_bundle, secret, answer.choices)
        for id_answer, encrypted_text_and_k in enumerate(encrypted_text_and_k_arr):
            individual_proof = AnswerUtility.compute_iprove(election_bundle.election, S, choices_for_a_question,
                                                            encrypted_text_and_k, id_answer, answer)
            answer.individual_proofs.append(individual_proof)

    # https://www.belenios.org/specification.pdf#subsubsection.4.11.1
    @staticmethod
    def generate_answer_for_h_question(election_uuid, blank_allowed, choices_for_a_question, secret):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        election = election_bundle.election
        if election is None:
            print("Invalid election")
            return None
        answer = AnswerHModel()
        encrypted_text_and_k_arr = []
        for id_answer, choice in enumerate(choices_for_a_question):
            m = choice
            encrypted_text_and_k = ElGamal().encrypt_from_int(m, election.public_key, election.group, save_k=True,
                                                              exponential=True)
            if len(encrypted_text_and_k.chunk) != 1:
                print("Error during encryption of the answer")
                return None

            encrypted_text_and_k_arr.append(encrypted_text_and_k)
            ciphertext_model = CiphertextModel()
            ciphertext_model.alpha = encrypted_text_and_k.chunk[0][0]
            ciphertext_model.beta = encrypted_text_and_k.chunk[0][1]
            answer.choices.append(ciphertext_model)
        AnswerUtility.compute_individuals_proofs(election_bundle, secret, answer, choices_for_a_question,
                                                 encrypted_text_and_k_arr)
        # TODO: implement iproov and ballot proof
        # if blank_allowed:
        #     print("blank not implemented yet")
        #     return None
        # else:
        #     # When a blank vote is not allowed, overall_proof proves that M ∈ [min . . . max] and is computed
        #     # by running iprove(S, R, M − min, min, . . . , max) where R is the sum of the r used in ciphertexts,
        #     # and M the sum of the m. There is no blank_proof.
        #     pass
        answer.overall_proof = ProofModel()
        answer.overall_proof.challenge = -1
        answer.overall_proof.response = -1

        return answer

    # https://www.belenios.org/specification.pdf#subsubsection.4.11.2
    @staticmethod
    def generate_answer_for_nh_question(election_uuid, choices, private_credential, public_credential, salt):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        election = election_bundle.election
        if election is None:
            print("Invalid election")
            return None

        # TODO: implement AnswerNh
        print("not implemented yet")
        return None

        answer = AnswerNhModel()
        answer.choices = CiphertextModel()
        xi = str([1 if answerStr == answerString else 0 for answerStr in question.answers]).encode()

        encrypted_text_and_k = ElGamal().encrypt(xi, election.public_key, election.group, save_k=True)
        if len(encrypted_text_and_k.chunk) != 1:
            print("Error during encryption of the answer")
            return None
        r = encrypted_text_and_k.chunk[0][0]
        answer.choices.alpha = encrypted_text_and_k.chunk[0][1]
        answer.choices.beta = encrypted_text_and_k.chunk[0][2]

        # IF multiple chunk is possible
        # if len(encrypted_text_and_k.chunk) > 0:
        #     print("Error during encryption of the answer")
        #     return None
        # r = [chunk[0] for chunk in encrypted_text_and_k.chunk]
        # answer.choices.alpha = [chunk[1] for chunk in encrypted_text_and_k.chunk]
        # answer.choices.beta = [chunk[2] for chunk in encrypted_text_and_k.chunk]
        # TODO: Check here
        # secret_c = Utility.derive_secret_exponent(credential, salt, election)
        # S0 = AnswerUtility.gen_S0(election_bundle, secret_c)

        S = ballot.credential
        # we generate A = g^w using a key pair, where private_key = A and public_key = w
        tmp = Utility.gen_key_el_gamal(election.group)
        w = tmp.private_key
        A = tmp.public_key

        challenge = ProofOfKnowledge.Hraweg(S, election, answer, A) % election.group.q
        response = (w - r * challenge)
        answer.proof = ProofModel()
        answer.proof.challenge = challenge
        answer.proof.response = response
        ballot.answers.append(answer)
        return ballot

    @staticmethod
    def check_single_nh_answer_proof(election_bundle, answer, credential):
        # TODO: Check here
        # secret_c = Utility.derive_secret_exponent(credential, salt, election_bundle.election)
        # S0 = AnswerUtility.gen_S0(election_bundle, secret_c)
        S = credential
        left = pow(election_bundle.election.group.g, answer.proof.response, election_bundle.election.group.p)
        right = pow(answer.choices.alpha, answer.proof.challenge, election_bundle.election.group.p)
        A = (left * right) % election_bundle.election.group.q
        challenge = ProofOfKnowledge.Hraweg(S, election_bundle.election, answer, A) % election_bundle.election.group.q
        return answer.proof.challenge == challenge

    @staticmethod
    def check_sign_ballot(election_uuid, ballot):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None

        left = pow(election_bundle.election.group.g, ballot.signature.proof.response, election_bundle.election.group.p)
        right = pow(ballot.credential, ballot.signature.proof.challenge, election_bundle.election.group.p)
        A = (left * right) % election_bundle.election.group.p
        H = ballot.signature.hash
        challenge = ProofOfKnowledge.Hsignature(H, A) % election_bundle.election.group.q
        return ballot.signature.proof.challenge == challenge

    @staticmethod
    def check_ballot(election_uuid, ballot, secret, choices_for_all_questions):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None

        # check the signature
        if not AnswerUtility.check_sign_ballot(election_uuid, ballot):
            return False

        # check iproof
        for id_answer, answer in enumerate(ballot.answers):
            S = AnswerUtility.gen_S(election_bundle, secret, answer.choices)
            for id_choice, choice in enumerate(answer.choices):
                if AnswerUtility.check_iprove(election_bundle.election, S, choices_for_all_questions[id_answer],
                                              id_answer, id_choice, answer):
                    print("invalid proof")
                    return False

        # TODO: check iproof
        # check blank_proof
        # check overall_proof
        # for answer in ballot.answers:
        #     if not AnswerUtility.check_single_nh_answer_proof(election_bundle, answer, ballot.credential):
        #         return False
        return True
