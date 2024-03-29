import json

from belenios.config.config import AppConfig
from belenios.core.belenios.ServerCore import ServerCore
from belenios.custom_types.belenios.EventType import EventType
from belenios.models.belenios.ElectionBundleModel import ElectionBundleModel
from belenios.models.belenios.ElectionModel import ElectionModel
from belenios.models.belenios.GroupModel import GroupModel
from belenios.models.belenios.QuestionHModel import QuestionHModel
from belenios.models.belenios.SetupDataModel import SetupDataModel
from belenios.models.belenios.SizedEncryptedTallyModel import SizedEncryptedTallyModel
from belenios.models.belenios.TallyModel import TallyModel
from belenios.models.belenios.VoterModel import VoterModel
from belenios.utilities.Utility import Utility
from belenios.utilities.command_line.AppObject import AppObject
from belenios.utilities.command_line.DbSession import DbSession


class ServerAdministratorCore:
    @staticmethod
    def start_new_election(name, description, administrator, credential_authority, group_name):
        # 1. A starts the preparation of an election,
        election_bundle = ElectionBundleModel()
        election_bundle.setup_data = SetupDataModel()
        # providing in particular the questions and the list of voters
        election = ElectionModel()
        election.version = 1
        election.name = name
        election.description = description
        election.public_key = None
        election.administrator = administrator
        election.credential_authority = credential_authority
        group = GroupModel()
        if AppConfig().el_gamal_groups.get(group_name, None) is None:
            AppObject().print("Group invalid")
            return None
        group.description = AppConfig().el_gamal_groups.get(group_name, None).description
        group.p = AppConfig().el_gamal_groups.get(group_name).p
        group.g = AppConfig().el_gamal_groups.get(group_name).g
        group.q = AppConfig().el_gamal_groups.get(group_name).q
        election.group = group
        election_bundle.election = election
        election_bundle.tally = TallyModel()
        election_bundle.tally.sized_encrypted_tally = SizedEncryptedTallyModel()
        DbSession().session.add(election_bundle)
        DbSession().session.commit()
        return election_bundle

    @staticmethod
    def add_question(election, question_text, answers, min, max, blank, ):
        question = QuestionHModel()
        question.question = question_text
        # question.answers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        question.answers = answers
        question.min = min
        question.max = max
        question.blank = blank
        election.questions.append(question)
        DbSession().session.commit()
        return question

    @staticmethod
    def add_voter(election_uuid, email, weight):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None, None

        # Check if a voter with the same email already exists
        existing_voter = DbSession().session.query(VoterModel).filter_by(email=email).first()
        if existing_voter:
            # Merge the existing voter with the election bundle
            election_bundle.voters.append(existing_voter)
            existing_voter.weight = weight  # Update the weight if necessary
            DbSession().session.commit()
            return existing_voter
        else:
            # Create a new voter
            new_voter = VoterModel(email=email, weight=weight)
            election_bundle.voters.append(new_voter)
            DbSession().session.commit()
            return new_voter

    # @staticmethod
    # def add_single_trustees(election_uuid, count):
    #     election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
    #     if election_bundle is None:
    #         print("Election uuid invalid")
    #         return None, None
    #     ServerCore().generates_trustee_public_key(election_uuid, count)
    #     # 2. S checks γ
    #     # We can check is the key and the pok is correctly generated :
    #     if TrusteesKeysProtocol().check_proof_trustee_key(election_bundle.election,
    #                                                       single_trustee.trustee_public_key):
    #         print("Trustee key is valid")
    #     else:
    #         print("Trustee key is invalid")
    #         return False
    #     return

    @staticmethod
    def check_perdersen_trustee_voutput(election_uuid, trustee_id, voutput):
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
            print("Invalid trustee id")
            return None
        prod = 1
        for i in range(len(pedersen_trustee.certs)):
            A_i = json.loads(election_bundle.polynomials[i].coefexps.signed_object.value)
            # print(A_i)
            for k in range(pedersen_trustee.threshold):
                jk = pow(trustee_id, k)
                A_ik = A_i[k]
                # print(A_ik)
                prod *= pow(A_ik, jk, election_bundle.election.group.p)
                prod = prod % election_bundle.election.group.p
        if voutput.trustee_public_key.public_key != prod:
            print("Invalid public key")
            return False
        return True


    @staticmethod
    def end_ballot(election_uuid):
        election_bundle = Utility.get_election_bundle_from_uuid(election_uuid)
        if election_bundle is None:
            print("Election uuid invalid")
            return None
        event = Utility.put_new_event(election_bundle)
        event.type = EventType.EndBallots
        DbSession().session.commit()
        return event
    @staticmethod
    def make_server_make_encrypted_tally(election_uuid):
        return ServerCore.compute_encrypted_tally(election_uuid)
    @staticmethod
    def make_server_compute_result(election_uuid):
        return ServerCore.compute_encrypted_tally(election_uuid)