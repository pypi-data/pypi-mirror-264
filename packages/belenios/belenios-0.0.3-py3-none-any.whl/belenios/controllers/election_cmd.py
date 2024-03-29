import json

from cement import Controller, ex
from cement.utils import shell

from belenios.core.belenios.ServerAdministratorCore import ServerAdministratorCore
from belenios.core.belenios.ServerCore import ServerCore
from belenios.core.belenios.TrusteeCore import TrusteeCore
from belenios.core.belenios.VoterCore import VoterCore


class ElectionCmd(Controller):
    class Meta:
        label = 'election'
        stacked_on = 'base'
        stacked_type = 'nested'
        # base_controller = True

        # text displayed at the top of --help output
        description = 'Belenios command-line tool to create and setup an election.'

        # text displayed at the bottom of --help output
        epilog = 'Usage: belenios election'

        arguments = [
            # (['-start', '--start'],
            #  {'action': 'start',
            #   '': }),
        ]


    @ex(
        help='Print the election bundle',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
        ],
    )
    def print_election(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        ServerCore().print_election_bundle(self.app.pargs.uuid)


    @ex(
        help='Generate ballot of the voter for the election',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
            (['-c', '--choices'], {'help': 'The choices of the voter for the election', 'action': 'store', 'dest': 'choices'}),
            (['-p', '--privcred'], {'help': 'The private credential of the voter for the election', 'action': 'store', 'dest': 'privcred'}),
        ],
    )
    def generate_ballot(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        if not self.app.pargs.choices:
            self.app.pargs.choices = shell.Prompt("Enter the choices of the voter for the election: ").input

        if not self.app.pargs.privcred:
            self.app.pargs.privcred = shell.Prompt("Enter the private credential of the voter for the election: ").input

        choices = json.loads(self.app.pargs.choices)
        if not VoterCore().check_choices_structure(self.app.pargs.uuid,choices ):
            print("Choice invalid")
            return False

        ballot = VoterCore().generate_ballot(self.app.pargs.uuid, choices, self.app.pargs.privcred)
        if ballot is None:
            print("Ballot not created")
            return False
        tally = ServerCore.add_to_tally(self.app.pargs.uuid, ballot)
        if tally is None:
            self.print("Tally invalid")
            return False
        print("Ballot created.")
        return True

    @ex(
        help='Close the election',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
        ],
    )
    def end_ballot(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input
        event = ServerAdministratorCore.end_ballot(self.app.pargs.uuid)
        if event is None:
            print("Election not closed.")
        print("Election closed.")
        return True

    @ex(
        help='Compute the encrypted tally of the election',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
        ],
    )
    def compute_encrypted_tally(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        tally = ServerAdministratorCore.make_server_make_encrypted_tally(self.app.pargs.uuid)
        if tally is None:
            print("Encrypted tally not computed.")
            return False
        event = ServerCore.set_event_encrypted_tally(self.app.pargs.uuid)
        if event is None:
            print("Encrypted tally not computed.")
            return False
        print("Encrypted tally computed.")
        return True

    @ex(
        help='Decrypt partially the encrypted tally of the election',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
            (['-fprk', '--file-private-key'],
             {'help': 'The file where to input private key of the trustee', 'action': 'store',
              'dest': 'file_private_key'}),
            (['-t', '--trustee-id'],
             {'help': 'The trustee id for the election', 'action': 'store', 'dest': 'trustee_id'}),
        ],
    )
    def decrypt(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        if not self.app.pargs.file_private_key:
            self.app.pargs.file_private_key = shell.Prompt(
                "Enter the file where to input private key of the trustee: ").input

        if not self.app.pargs.trustee_id:
            self.app.pargs.trustee_id = shell.Prompt("Enter the trustee id for the election: ").input

        try:
            with open(self.app.pargs.file_private_key, 'r') as file:
                data = json.load(file)
        except:
            print("Invalid private key file")
            return False

        owned_partial_decryption = TrusteeCore.partial_decrypt_encrypted_ballot(self.app.pargs.uuid, int(data),
                                                                                int(self.app.pargs.trustee_id))
        if owned_partial_decryption is None:
            print("Encrypted tally not partially decrypted.")
            return False
        event = ServerCore.add_event_partial_decryption(self.app.pargs.uuid)
        if event is None:
            print("Encrypted tally partially decrypted.")
        print("Encrypted tally partially decrypted.")
        return True

    @ex(
        help='Decrypt partially the encrypted tally with threshold of the election',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
            (['-fprk', '--file-private-key'],
             {'help': 'The file where to input private key of the trustee', 'action': 'store',
              'dest': 'file_private_key'}),
            (['-t', '--trustee-id'],
             {'help': 'The trustee id for the election', 'action': 'store', 'dest': 'trustee_id'}),
            (['-dk', '--decryption-key'],
             {'help': 'The file where to output the decryption key for trustee key decryption', 'action': 'store',
              'dest': 'file_decryption_key'}),
        ],
    )
    def decrypt_threshold(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        if not self.app.pargs.file_private_key:
            self.app.pargs.file_private_key = shell.Prompt(
                "Enter the file where to input private key of the trustee: ").input

        if not self.app.pargs.trustee_id:
            self.app.pargs.trustee_id = shell.Prompt("Enter the trustee id for the election: ").input

        if not self.app.pargs.file_decryption_key:
            self.app.pargs.file_decryption_key = shell.Prompt("Enter file where to output the decryption key: ").input

        try:
            with open(self.app.pargs.file_decryption_key, 'r') as file:
                decryption_key = json.load(file)
        except:
            print("Invalid private key file")
            return False

        owned_partial_decryption = TrusteeCore.partial_decrypt_encrypted_ballot(self.app.pargs.uuid, int(decryption_key),
                                                                                int(self.app.pargs.trustee_id))
        if owned_partial_decryption is None:
            print("Encrypted tally not partially decrypted.")
            return False
        event = ServerCore.add_event_partial_decryption(self.app.pargs.uuid)
        if event is None:
            print("Encrypted tally partially decrypted.")
        print("Encrypted tally partially decrypted.")
        return True

    @ex(
        help='Compute the result of the election',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
        ],
    )
    def compute_result(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        result = ServerCore.compute_result(self.app.pargs.uuid)
        if result is None:
            print("The result was not computed.")
            return False
        event = ServerCore.set_event_result(self.app.pargs.uuid)
        if event is None:
            print("The result was not computed.")
        print("The result was computed.")
        return True

    @ex(
        help='Show the array of result of the election',

        # sub-command level arguments.
        arguments=[
            (['-u', '--uuid'], {'help': 'The uuid of the election', 'action': 'store', 'dest': 'uuid'}),
        ],
    )
    def show_result(self):
        if not self.app.pargs.uuid:
            self.app.pargs.uuid = shell.Prompt("Enter the uuid of the election: ").input

        result = ServerCore.get_array_of_result(self.app.pargs.uuid)
        if result is None:
            print("The array of result was not computed.")
            return False
        print(result)
        return True
