__author__ = 'admin'

from utilities.compile import compile
from docopt import docopt

# Define the command line interface:
commands = """
Usage:
    main.py compile [--template=TEMPLATE] [--dump==DUMPFILE]

Options:
    -t, --template=TEMPLATE     the template for compiling process [default: template.apib]
    -d, --dump=DUMPFILE         the destination for the compiling process [default: apiary.apib]
"""


if __name__ == '__main__':
    # get the input args from docopt:
    arguments = docopt(commands, argv=None, help=True, version=None, options_first=False)

    if arguments.get('compile'):
        template = arguments.get('--template')
        dumpfile = arguments.get('--dump')
        print('Compiling with template: %s to %s\n' % (template, dumpfile))
        compile(tempalte=template, dumpfile=dumpfile)

    else:
        assert False, 'The operation not supported'
