__author__ = 'admin'

import os
from utilities.compile import compile
from utilities.version_update import version_update
from docopt import docopt


# Define the command line interface:
commands = """
Usage:
    main.py compile [--template=TEMPLATE] [--dump=DUMPFILE] [-g]
    main.py version_update [--target=TARGET] [-c] [--template=TEMPLATE] [--dump=DUMPFILE]

Options:
    -t, --template=TEMPLATE     the template for compiling process [default: template.apib]
    -d, --dump=DUMPFILE         the destination for the compiling process [default: apiary.apib]
    --target=TARGET             the target file for version update [default: template.apib]
    -c                          should run the compile process after version update
    -g                          should commit the dump file after compilation
"""


if __name__ == '__main__':
    # get the input args from docopt:
    arguments = docopt(commands, argv=None, help=True, version=None, options_first=False)

    if arguments.get('compile'):
        template = arguments.get('--template')
        dumpfile = arguments.get('--dump')
        commit_after_compilation = arguments.get('-g')

        print('Compiling with template: %s to %s\n' % (template, dumpfile))
        compile(tempalte=template, dumpfile=dumpfile)

        if commit_after_compilation:
            print('\nStart committing the result: %s' % dumpfile)
            os.system('git commit %s' % dumpfile)

    elif arguments.get('version_update'):
        target = arguments.get('--target')
        should_compile = arguments.get('-c')

        version_update(target=target)
        if should_compile:
            template = arguments.get('--template')
            dumpfile = arguments.get('--dump')
            compile(template=template, dumpfile=dumpfile)

    else:
        assert False, 'The operation not supported'
