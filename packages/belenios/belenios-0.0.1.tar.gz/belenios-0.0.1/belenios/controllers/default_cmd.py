from cement import Controller
from cement.utils.version import get_version_banner

from belenios.core.command_line.version import get_version

VERSION_BANNER = """
This is a proof of concept of the Belenios election protocol. %s
%s
""" % (get_version(), get_version_banner())


class DefaultCmd(Controller):
    class Meta:
        label = 'base'

        # base_controller = True

        # text displayed at the top of --help output
        description = 'This is a proof of concept of the Belenios election protocol.'

        # text displayed at the bottom of --help output
        epilog = 'Usage: belenios'

        # controller level arguments. ex: 'belenios --version'
        arguments = [
            ### add a version banner
            (['-v', '--version'],
             {'action': 'version',
              'version': VERSION_BANNER}),
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()
