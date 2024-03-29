from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal


from belenios.controllers.default_cmd import DefaultCmd
from belenios.controllers.election_cmd import ElectionCmd
from belenios.controllers.setup_cmd import SetupCmd
from belenios.core.command_line.exc import BeleniosError
from belenios.models.BaseModel import BaseModel
from belenios.utilities.DatabaseInit import DatabaseInit
from belenios.utilities.command_line.AppObject import AppObject


# configuration defaults

def post_setup(app):
    AppObject().addApp(app)


class Belenios(App):
    """Belenios primary application."""

    class Meta:
        label = 'belenios'

        config_files = ['config.yml']

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
            'jinja2',
        ]

        hooks = [
            ('post_setup', post_setup),
        ]
        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'jinja2'

        base_controller = DefaultCmd
        # register handlers
        handlers = [
            DefaultCmd,
            SetupCmd,
            ElectionCmd,
        ]


class BeleniosTest(TestApp, Belenios):
    """A sub-class of Belenios that is better suited for testing."""

    class Meta:
        label = 'belenios'


def main():
    with Belenios() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except BeleniosError as e:
            print('BeleniosError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
