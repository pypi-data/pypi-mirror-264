import json

from cement import Controller, ex
from cement.utils import shell

from belenios.core.belenios.CredentialAuthorityCore import CredentialAuthorityCore
from belenios.core.belenios.ServerAdministratorCore import ServerAdministratorCore
from belenios.core.belenios.ServerCore import ServerCore
from belenios.core.belenios.TrusteeCore import TrusteeCore
from belenios.models.belenios.ProofModel import ProofModel
from belenios.models.belenios.QuestionHModel import QuestionHModel
from belenios.models.belenios.QuestionNhModel import QuestionNhModel
from belenios.models.belenios.TrusteePublicKeyModel import TrusteePublicKeyModel
from belenios.models.belenios.VInputModel import VInputModel


class SetupCmd(Controller):
    class Meta:
        label = 'setup'
        stacked_on = 'base'
        stacked_type = 'nested'
        # base_controller = True

        # text displayed at the top of --help output
        description = 'Belenios command-line tool to create and setup an election.'

        # text displayed at the bottom of --help output
        epilog = 'Usage: belenios setup'

        arguments = [
            # (['-start', '--start'],
            #  {'action': 'start',
            #   '': }),
        ]

    # @ex(
    #     help='login',
    #
    #     # sub-command level arguments.
    #     arguments=[
    #         (['-u', '--username'],
    #          {'help': 'The username to login', 'action': 'store', 'dest': 'username', 'required': True}),
    #         (['-p', '--password'],
    #          {'help': 'The password to login', 'action': 'store', 'dest': 'password', 'required': True}),
    #     ],
    # )
    # def login(self):
    #     print("login :", self.app.pargs.username, self.app.pargs.password)
    #     # Retrieve username and password from command-line arguments
    #     username = self.app.pargs.username
    #     password = self.app.pargs.password
    #
    #     # Store the session information
    #     print(UserSession().username)
    #
    #     print("Logged in successfully!")

    @ex(
        help='Start a new election creation',

        # sub-command level arguments.
        arguments=[
            (['-n', '--name'],
             {'help': 'The name of the election', 'action': 'store', 'dest': 'name'}),
            (['-d', '--description'],
             {'help': 'The description of the election', 'action': 'store', 'dest': 'description'}),
            (['-g', '--group'], {'help': 'The group of the election', 'action': 'store', 'dest': 'group'}),
            (['-a', '--administrator'],
             {'help': 'The email of the administrator of the election', 'action': 'store', 'dest': 'administrator'}),
            (['-c', '--credential_authority'],
             {'help': 'The email of the credential authority of the election', 'action': 'store',
              'dest': 'credential_authority'}),
        ],
    )
    def start(self):
        if not self.app.pargs.name:
            self.app.pargs.name = shell.Prompt("Enter the name of the election: ").input

        if not self.app.pargs.description:
            self.app.pargs.description = shell.Prompt("Enter the description of the election: ").input

        if not self.app.pargs.group:
            self.app.pargs.group = shell.Prompt("Enter the group of the election: ").input
        self.app.pargs.group = self.app.pargs.group.upper()

        if not self.app.pargs.administrator:
            self.app.pargs.administrator = shell.Prompt("Enter the email of the administrator: ").input

        if not self.app.pargs.credential_authority:
            self.app.pargs.credential_authority = shell.Prompt("Enter the email of the credential authority: ").input

        # Now you can proceed with the creation of the election using the provided inputs
        print("Starting election creation with the following parameters:")
        print("Name: %s" % self.app.pargs.name)
        print("Description: %s" % self.app.pargs.description)
        print("Group: %s" % self.app.pargs.group)
        print("Administrator: %s" % self.app.pargs.administrator)
        print("Credential Authority: %s" % self.app.pargs.credential_authority)

        election_bundle = ServerAdministratorCore.start_new_election(self.app.pargs.name, self.app.pargs.description,
                                                                     self.app.pargs.administrator,
                                                                     self.app.pargs.credential_authority,
                                                                     self.app.pargs.group)
        if election_bundle is None:
            self.print("Election not created")
            return False
        ServerCore().make_election_unique(election_bundle.election)

        print("New election created with uuid: %s" % election_bundle.election.uuid)

        return True

    @ex(
        help='Add a new voter to the election',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'],
             {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
            (['-e', '--email'],
             {'help': 'The email of the voter', 'action': 'store', 'dest': 'email'}),
            (['-w', '--weight'],
             {'help': 'The weight of the voter', 'action': 'store', 'dest': 'weight'}),
        ],
    )
    def add_voter(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        if not self.app.pargs.email:
            self.app.pargs.email = shell.Prompt("Enter the email of the new voter: ").input

        if not self.app.pargs.weight:
            self.app.pargs.weight = shell.Prompt("Enter the weight of the new voter: ").input

        print("Starting to add a new voter with the following parameters:")
        print("Uuid: %s" % self.app.pargs.uuid)
        print("Email: %s" % self.app.pargs.email)
        print("Weight: %s" % self.app.pargs.weight)

        voter = ServerAdministratorCore.add_voter(self.app.pargs.uuid, self.app.pargs.email,
                                                  self.app.pargs.weight, )
        if voter is None:
            self.print("Voter not created")
            return False

        print("New voter created.")
        return True

    @ex(
        help='Generate voters credentials and salts for the election',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
            (['-fprc', '--file-private-credentials'],
             {'help': 'The file where to output private credentials of the election', 'action': 'store',
              'dest': 'file_private_credentials'}),
            (['-fpuc', '--file-public-credentials'],
             {'help': 'The file where to output public credentials of the election', 'action': 'store',
              'dest': 'file_public_credentials'}),
            (['-fs', '--file--salts'],
             {'help': 'The file where to output salts of the election', 'action': 'store', 'dest': 'file_salts'}),
        ],
    )
    def generate_credentials(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        if not self.app.pargs.file_private_credentials:
            self.app.pargs.file_private_credentials = shell.Prompt(
                "Enter the file where to output private credentials of the election: ").input

        if not self.app.pargs.file_public_credentials:
            self.app.pargs.file_public_credentials = shell.Prompt(
                "Enter the file where to output public credentials of the election: ").input

        if not self.app.pargs.file_salts:
            self.app.pargs.file_salts = shell.Prompt("Enter the file where to output salts of the election: ").input

        print("Starting generation parameters:")
        print("uuid: %s" % self.app.pargs.uuid)

        # sending election.uuid to C
        private_credentials, public_credentials, salts = CredentialAuthorityCore().generate_voters_credentials_and_salts(
            self.app.pargs.uuid)

        if private_credentials is None or public_credentials is None or salts is None or len(salts) == 0 or len(
                private_credentials) != len(public_credentials) or len(public_credentials) != len(salts):
            print("Credentials and salts were not generated")
            return False

        if ServerCore().check_voters_credentials_and_salts(self.app.pargs.uuid, public_credentials, salts):
            print("The voting server checked email, weight, public credentials and salts.")
        else:
            print("The voting server detected an error in public data")
            return False

        with open(self.app.pargs.file_private_credentials, 'w') as file:
            json.dump(private_credentials, file)

        with open(self.app.pargs.file_public_credentials, 'w') as file:
            json.dump(public_credentials, file)

        with open(self.app.pargs.file_salts, 'w') as file:
            json.dump(salts, file)

        print("Credentials and salts generated for %s voters." % len(private_credentials))
        return True

    @ex(
        help='Generate a trustees key for the election',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
            (['-fprk', '--file-private-key'],
             {'help': 'The file where to output private key of the trustee', 'action': 'store',
              'dest': 'file_private_key'}),
            (['-fpuk', '--file-public-key'],
             {'help': 'The file where to output public key of the trustee', 'action': 'store',
              'dest': 'file_public_key'}),
        ],
    )
    def generate_trustee_key(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        if not self.app.pargs.file_private_key:
            self.app.pargs.file_private_key = shell.Prompt(
                "Enter file where to output private key of the trustee: ").input

        if not self.app.pargs.file_public_key:
            self.app.pargs.file_public_key = shell.Prompt(
                "Enter file where to output public key of the trustee: ").input

        print("Starting generation parameters:")
        print("uuid: %s" % self.app.pargs.uuid)

        # trustees = trustee_kind∗
        # trustee_kind = ["Single", trustee_public_key] | ["Pedersen", threshold_parameters]
        # [["Single", . . . ], ["Single", . . . ], ["Single", . . . ]]
        # 8. S defines the shape of the trustees structure that will be used in the election depending
        # on A’s instructions;
        # TODO: use A’s instructions;

        # 9. S and T1, . . . , Tm run key establishment protocols (see 3.1.1) as needed to fill in the trustees
        # structure;

        # "Single" protocol :

        # 1. T generates a trustee_public_key γ and sends it to S
        trustee_public_key, keys_pair = TrusteeCore().generates_single_trustee_public_key(self.app.pargs.uuid)
        if trustee_public_key is None or keys_pair is None:
            print("The key was not created.")

        with open(self.app.pargs.file_private_key, 'w') as file:
            json.dump(keys_pair.private_key, file)

        with open(self.app.pargs.file_public_key, 'w') as file:
            json.dump(trustee_public_key.to_json(), file)
        print("Trustee key generated.")
        return True

    @ex(
        help='Generate a threshold trustees key for the election',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
            (['-fprk', '--file-private-key'],
             {'help': 'The file where to output private key of the trustee', 'action': 'store',
              'dest': 'file_private_key'}),
            (['-fc', '--file-cert'],
             {'help': 'The file where to output cert of the trustee', 'action': 'store',
              'dest': 'file_cert'}),
            (['-s', '--step'],
             {'help': 'The step of the Perdersen trustee key generation', 'action': 'store',
              'dest': 'step'}),
            (['-tid', '--trustee-id'],
             {'help': 'The trustee id for the election', 'action': 'store', 'dest': 'trustee_id'}),
            (['-t', '--threshold'],
             {'help': 'The threshold need for trustee key decryption', 'action': 'store', 'dest': 'threshold'}),
            (['-vi', '--vinput'],
             {'help': 'The file where to input the verification data for trustee key decryption', 'action': 'store',
              'dest': 'file_vinput'}),
            (['-vo', '--voutput'],
             {'help': 'The file where to output the verification data for trustee key decryption', 'action': 'store',
              'dest': 'file_voutput'}),
            (['-dk', '--decryption-key'],
             {'help': 'The file where to output the decryption key for trustee key decryption', 'action': 'store',
              'dest': 'file_decryption_key'}),
        ],
    )
    def generate_trustee_key_threshold(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        if not self.app.pargs.file_private_key:
            self.app.pargs.file_private_key = shell.Prompt(
                "Enter file where to output private key of the trustee: ").input

        if not self.app.pargs.step:
            self.app.pargs.step = shell.Prompt("Enter step of the Perdersen trustee key generation: ").input
        self.app.pargs.step = int(self.app.pargs.step)

        if not self.app.pargs.trustee_id:
            self.app.pargs.trustee_id = shell.Prompt("Enter the trustee id for the election: ").input
        self.app.pargs.trustee_id = int(self.app.pargs.trustee_id)

        print("Starting generation parameters:")
        print("uuid: %s" % self.app.pargs.uuid)
        print("step: %s" % self.app.pargs.step)

        # trustees = trustee_kind∗
        # trustee_kind = ["Single", trustee_public_key] | ["Pedersen", threshold_parameters]
        # [["Single", . . . ], ["Single", . . . ], ["Single", . . . ]]
        # 8. S defines the shape of the trustees structure that will be used in the election depending
        # on A’s instructions;
        # TODO: use A’s instructions;

        # 9. S and T1, . . . , Tm run key establishment protocols (see 3.1.1) as needed to fill in the trustees
        # structure;

        # "Perdersen" protocol :

        if self.app.pargs.step == 1:  # and 2 actually

            if not self.app.pargs.file_cert:
                self.app.pargs.file_cert = shell.Prompt(
                    "Enter file where to output cert of the trustee: ").input

            # (a) Tz generates a cert γz and sends it to S
            signed_msg, seed = TrusteeCore().generates_perdersen_trustee_keys(self.app.pargs.uuid)
            if signed_msg is None or seed is None:
                print("The cert was not created.")
            print("The cert has been created.")

            # ttkeygen --certs certs.jsons --step 2
            pedersen_trustee = ServerCore.import_cert_pedersen_trustee(self.app.pargs.uuid, signed_msg,
                                                                     self.app.pargs.trustee_id)
            if pedersen_trustee is None:
                print("The cert was not imported.")
                return False
            print("The cert has been imported.")

            with open(self.app.pargs.file_private_key, 'w') as file:
                json.dump(seed, file)

            with open(self.app.pargs.file_cert, 'w') as file:
                json.dump(signed_msg.to_dict(), file)
        elif self.app.pargs.step == 3:
            if not self.app.pargs.threshold:
                self.app.pargs.threshold = shell.Prompt("Enter the threshold need for trustee key decryption: ").input
            self.app.pargs.threshold = int(self.app.pargs.threshold)
            try:
                with open(self.app.pargs.file_private_key, 'r') as file:
                    seed = json.load(file)
            except:
                print("Invalid private key file")
                return False

            polynomial = TrusteeCore.generates_perdersen_trustee_polynomial(self.app.pargs.uuid,
                                                                            self.app.pargs.threshold, seed,
                                                                            self.app.pargs.trustee_id)
            if polynomial is None:
                print("The polynomial was not created.")
                return False
            print("The polynomial has been created.")
        elif self.app.pargs.step == 4:
            if not self.app.pargs.file_vinput:
                self.app.pargs.file_vinput = shell.Prompt("Enter file where to input the verification data: ").input

            # if not self.app.pargs.threshold:
            #     self.app.pargs.threshold = shell.Prompt("Enter the threshold need for trustee key decryption: ").input
            # self.app.pargs.threshold = int(self.app.pargs.threshold)
            # if not self.app.pargs.file_voutput:
            #     self.app.pargs.file_voutput = shell.Prompt("Enter file where to output the verification data: ").input
            try:
                with open(self.app.pargs.file_private_key, 'r') as file:
                    seed = json.load(file)
            except:
                print("Invalid private key file")
                return False
            vinput = TrusteeCore.generates_perdersen_trustee_vinput(self.app.pargs.uuid, seed,
                                                                    self.app.pargs.trustee_id)

            if vinput is None:
                print("The vinput was not created.")
                return False
            print("The vinput has been created.")
            check = TrusteeCore.check_perdersen_trustee_vinput(self.app.pargs.uuid, seed, self.app.pargs.trustee_id,
                                                               vinput)

            if check != True:
                print("The vinput was not correctly generated.")
                return False

            with open(self.app.pargs.file_vinput, 'w') as file:
                json.dump(vinput.to_dict(), file)
        elif self.app.pargs.step == 5:
            if not self.app.pargs.file_vinput:
                self.app.pargs.file_vinput = shell.Prompt("Enter file where to input the verification data: ").input

            if not self.app.pargs.file_voutput:
                self.app.pargs.file_voutput = shell.Prompt("Enter file where to output the verification data: ").input

            if not self.app.pargs.file_decryption_key:
                self.app.pargs.file_decryption_key = shell.Prompt(
                    "Enter file where to output the decryption key: ").input
            try:
                with open(self.app.pargs.file_private_key, 'r') as file:
                    seed = json.load(file)
            except:
                print("Invalid private key file")
                return False

            try:
                with open(self.app.pargs.file_vinput, 'r') as file:
                    vinput_json = json.load(file)

            except Exception as e:
                print("Invalid private key file")
                print(e)
                return False
            v_input = VInputModel.load_from_json(vinput_json)
            voutput, private_key = TrusteeCore.generates_perdersen_trustee_voutput(self.app.pargs.uuid, seed,
                                                                      self.app.pargs.trustee_id, v_input)

            if voutput is None:
                print("The voutput was not created.")
                return False
            print("The voutput has been created.")

            check = ServerAdministratorCore.check_perdersen_trustee_voutput(self.app.pargs.uuid,
                                                                            self.app.pargs.trustee_id, voutput)

            if check != True:
                print("The voutput was not correctly generated.")
                return False

            pedersen_trustee = ServerCore.import_coefexps_verification_keys_pedersen_trustee(self.app.pargs.uuid,
                                                                                             voutput)
            if pedersen_trustee is None:
                print("The verification_key was not imported.")
                return False
            print("The verification_key has been imported.")

            with open(self.app.pargs.file_voutput, 'w') as file:
                json.dump(voutput.to_dict(), file)
            with open(self.app.pargs.file_decryption_key, 'w') as file:
                json.dump(private_key, file)
        #     TODO: admin check public_key
        # TODO: check if step 6 is already done
        else:
            print("step invalid")
            return False
        return True

    @ex(
        help='Send a trustees key to the server for the election',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
            (['-fpuk', '--file-public-key'],
             {'help': 'The file where to output public key of the trustee', 'action': 'store',
              'dest': 'file_public_key'}),
            (['-tid', '--trustee-id'],
             {'help': 'The trustee id for the election', 'action': 'store', 'dest': 'trustee_id'}),
        ],
    )
    def send_trustee_key(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        if not self.app.pargs.file_public_key:
            self.app.pargs.file_public_key = shell.Prompt(
                "Enter file where to output public key of the trustee: ").input

        if not self.app.pargs.trustee_id:
            self.app.pargs.trustee_id = shell.Prompt("Enter the id of the trustee for the election: ").input

        print("Starting generation parameters:")
        print("uuid: %s" % self.app.pargs.uuid)

        try:
            with open(self.app.pargs.file_public_key, 'r') as file:
                data = json.load(file)
            trustee_public_key = TrusteePublicKeyModel()
            trustee_public_key.public_key = data['public_key']
            proof = ProofModel()
            proof.challenge = data["pok"]['challenge']
            proof.response = data["pok"]['response']
            trustee_public_key.pok = proof
        except:
            print("Invalid file")
            return False
        single_trustee = ServerCore.import_public_key_single_trustee(self.app.pargs.uuid, trustee_public_key,
                                                                     self.app.pargs.trustee_id)
        if single_trustee is None:
            print("The key was not imported.")
            return False
        print("The key has been imported.")
        return True

    @ex(
        help='Make the election structure and calculate hash to make it immutable',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
            (['-t', '--template'],
             {'help': 'The template of the questions of the election', 'action': 'store', 'dest': 'template'}),
        ],
    )
    def make_election(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        if not self.app.pargs.template:
            self.app.pargs.template = shell.Prompt("Enter the template of the questions of the election: ").input

        print("Starting generation parameters:")
        print("uuid: %s" % self.app.pargs.uuid)
        print("template: %s" % self.app.pargs.template)

        election_bundle = ServerCore.compute_election_public_key(self.app.pargs.uuid)
        if election_bundle is None:
            print("The election was not created.")
        questions = []
        try:
            with open(self.app.pargs.template, 'r') as file:
                data = json.load(file)
            for i, question_data in enumerate(data):
                print("Adding question:", question_data)
                if question_data.get('type', 'QuestionHModel') == 'QuestionNhModel':
                    question = QuestionNhModel()
                    question.answers = question_data["answers"]
                    question.question = question_data["question"]
                else:
                    question = QuestionHModel()
                    question.answers = question_data["answers"]
                    question.min = question_data.get("min", 0)
                    question.max = question_data.get("max", 0)
                    question.blank = question_data.get("blank", False)
                    question.question = question_data.get("question", "Question?")
                questions.append(question)
        except:
            print("Invalid file")
            return False

        questions = ServerCore.add_questions(self.app.pargs.uuid, questions)
        if questions is None:
            print("The election was not created.")

        election_bundle = ServerCore.make_election_immutable(self.app.pargs.uuid)
        if election_bundle is None:
            print("The election was not created.")

        print("The election has been created.")
        # TODO: handle adding it to event
        return True
