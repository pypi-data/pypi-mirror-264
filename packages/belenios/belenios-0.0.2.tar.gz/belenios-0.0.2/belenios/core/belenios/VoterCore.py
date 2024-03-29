from belenios.models.belenios.BallotModel import BallotModel
from belenios.models.belenios.ProofModel import ProofModel
from belenios.models.belenios.SignatureModel import SignatureModel
from belenios.utilities.AnswerUtility import AnswerUtility
from belenios.utilities.ProofOfKnowledge import ProofOfKnowledge
from belenios.utilities.Utility import Utility
from belenios.utilities.command_line.DbSession import DbSession


class VoterCore:
    @staticmethod
    def get_public_credential_from_index(election_uuid, index):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        for credential in election_bundle.public_credentials:
            if credential.index == index:
                return credential

    @staticmethod
    def get_salt_from_private_credential(election_uuid, index):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        for salt in election_bundle.salts:
            if salt.index == index:
                return salt

    @staticmethod
    def check_choices_structure(election_uuid, choices):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return False
        # check type of choice ([[int, int,...], [int, int,...], [blank, int,...], ...])
        if not isinstance(choices, list):
            return False
        for c in choices:
            if not isinstance(c, list):
                return False
            for a in c:
                if not isinstance(a, int):
                    return False
        if len(choices) != len(election_bundle.election.questions):
            return False

        # validing the size of sub-arrays and correct blank vote
        for i, choice in enumerate(choices):
            question = election_bundle.election.questions[i]
            if question.type == "QuestionHModel":
                if question.blank:
                    if len(choice) != len(question.answers) + 1:
                        return False
                    if choice[0] == 1:  # it a blank vote
                        for a in choice[1:]:
                            if a != 0:
                                return False
                    else:
                        for a in choice:
                            if a not in [0, 1]:
                                return False
                        if not (question.min <= choice[1:].count(1) <= question.max):
                            return False
                else:
                    if len(choice) != len(question.answers):
                        return False
                    for a in choice:
                        if a not in [0, 1]:
                            return False
                    if not (question.min <= choice.count(1) <= question.max):
                        return False
            else:  # "type": "QuestionNhModel"
                if len(choice) != len(question.answers):
                    return False
                for a in choice:
                    if a not in [0, 1]:
                        return False
        return True

    @staticmethod
    def sign_ballot(election_uuid, ballot, x):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None

        # we generate A = g^w using a key pair, where private_key = A and public_key = w
        tmp = Utility.gen_key_el_gamal(election_bundle.election.group)
        w = tmp.private_key
        A = tmp.public_key
        H = ballot.to_hash_sha256()
        challenge = ProofOfKnowledge.Hsignature(H, A) % election_bundle.election.group.q
        response = (w - x * challenge)
        ballot.signature = SignatureModel()
        ballot.signature.hash = H
        ballot.signature.proof = ProofModel()
        ballot.signature.proof.challenge = challenge
        ballot.signature.proof.response = response
        return ballot

    @staticmethod
    def generate_ballot(election_uuid, choices_for_all_questions, private_credential):
        # 1. V gets public data of E
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None

        prefix, index = Utility.get_prefix_index_from_credential(private_credential)

        # 2. V uses the index in her secret credential c to get her public credential ˆc (from election public
        # data) and her salt s (from salts), and checks that ˆc = public(c, s)

        # getting public credential from election bundle
        public_credential = VoterCore.get_public_credential_from_index(election_uuid, index)
        if public_credential is None:
            print("Credential invalid")
        # getting salt from election bundle
        salt = VoterCore.get_salt_from_private_credential(election_uuid, index)
        if salt is None:
            print("Credential invalid")

        # check that public credential ^c is ok
        x = Utility.derive_secret_exponent(prefix, salt, election_bundle.election)
        if str(pow(election_bundle.election.group.g, x,
               election_bundle.election.group.p)) != str(public_credential.public_credential):  # Calculate g^x mod p
            print("Credential invalid")

        ballot = BallotModel()
        ballot.election_uuid = election_bundle.election.uuid
        ballot.election_hash = election_bundle.setup_data.election
        ballot.credential = int(public_credential.public_credential)

        prefix, index = Utility.get_prefix_index_from_credential(private_credential)
        secret = Utility.derive_secret_exponent(prefix, salt, election_bundle.election)
        # Try to make a vote :
        # TODO: check if we need to have the private of public key
        # ballot = AnswerUtility.generate_single_nh_answer(self.app, election_bundle, question, "Non",
        #                                                     UnsafelyStoringCredentials().credentials[0], salts[0])
        for i, question in enumerate(election_bundle.election.questions):
            if question.type == "QuestionHModel":
                answer = AnswerUtility.generate_answer_for_h_question(election_uuid, question.blank,
                                                                      choices_for_all_questions[i], secret)
                if answer is None:
                    return None
                else:
                    ballot.answers.append(answer)
            else:
                answer = AnswerUtility.generate_answer_for_nh_question(election_uuid, choices_for_all_questions[i],
                                                                       private_credential, public_credential, salt)
                if answer is None:
                    return None
                else:
                    ballot.answers.append(answer)
        # TODO: add verification of the ballot and a command to send it separately
        # 4. S processes b:
        # (a) let C be the public credential used in b (its credential field)
        # (b) S checks that (C, wi, V) ∈ L
        # (c) S checks all zero-knowledge proofs of b
        # (d) S adds b to D
        # 5. at any time (even after tally), V may check that h (if it is her last ballot) appears in the list
        # of pretty ballots P B and the weight of her ballot as it appears in P B is equal to her weight
        DbSession().session.add(ballot)
        VoterCore.sign_ballot(election_uuid, ballot, x)

        # We can check is the answer and the proof is correctly generated :
        if AnswerUtility.check_ballot(election_uuid, ballot,secret, choices_for_all_questions):
            print("Proof is valid")
        else:
            print("Proof is invalid")
            return None

        DbSession().session.commit()
        return ballot
