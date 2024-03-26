from pprint import pformat

from rlpython.utils.argument_parser import ReplArgumentParser
from rlpython.utils.table import write_table

from lona import VERSION_STRING


class LonaInfoCommand:
    """
    Show Lona info
    """

    NAME = 'lona_info'

    def __init__(self, repl):
        self.repl = repl

    def run(self, argv):
        # parse command line
        argument_parser = ReplArgumentParser(repl=self.repl, prog='lona_info')

        argument_parser.parse_args(argv[1:])

        # write version string
        rows = [
            ['Key', 'Value'],
            ['Lona version', f'v{VERSION_STRING}'],
            ['project root', self.repl.globals['server'].project_root],
            ['cli args', pformat(self.repl.globals.get('cli_args', {}))],

            ['logging syslog priorities',
             repr(self.repl.globals['log_formatter'].syslog_priorities)],
        ]

        write_table(rows, self.repl.write)
