import argparse

from . import __version__

parser = argparse.ArgumentParser(prog='gourmand',
                                 description=__version__.description)
parser.add_argument('--version',
                    action='version',
                    version=__version__.version)
parser.add_argument('--database-url',
                    action='store',
                    dest='db_url',
                    help='Database uri formatted like driver://path/to/db',
                    default='')
parser.add_argument('--use-threads',
                    action='store_const',
                    const=True,
                    dest='threads',
                    help='Enable threading support.',
                    default=False)
parser.add_argument('--disable-threads',
                    action='store_const',
                    const=False,
                    dest='threads',
                    help='Disable threading support.')
parser.add_argument('--gourmand-directory',
                    action='store',
                    dest='gourmanddir',
                    help='Gourmand configuration directory',
                    default='')
parser.add_argument('--debug-threading-interval',
                    action='store',
                    type=float,
                    dest='thread_debug_interval',
                    help='Interval for threading debug calls',
                    default=5.0)
parser.add_argument('--debug-threading',
                    action='store_true',
                    dest='thread_debug',
                    help='Print debugging information about threading.')
parser.add_argument('--debug-file',
                    action='store',
                    dest='debug_file',
                    help=('Regular expression that matches filename(s) '
                          'containing code for which we want to display '
                          'debug messages.'),
                    default='')
parser.add_argument('--showtimes',
                    action='store_true',
                    dest='time',
                    help='Print timestamps on debug statements.')

group = parser.add_mutually_exclusive_group()
group.add_argument('-q',
                   action='store_const',
                   const=-1,
                   dest='debug',
                   help='Do not print gourmand error messages')
group.add_argument('-v',
                   action='count',
                   dest='debug',
                   help="Be verbose (extra v's increase the verbosity level)")

args = parser.parse_known_args()[0]
print(f"args = {args}")
