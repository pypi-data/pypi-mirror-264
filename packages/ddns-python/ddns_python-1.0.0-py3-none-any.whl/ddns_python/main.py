#!/usr/bin/python3
#

from .console_menu import MenuConfig
from .constants import GLOBALS
from .test_configuration import test_configuration
from .update import Update
from .utils import Tempfolder

from sys import stderr

def main():
    print('%s by @9Lukas5 started' % GLOBALS['program_name'])

    MenuConfig.init()

    # if subfunction
    if MenuConfig.args.test_configuration:
        exit(test_configuration())

    def get_subprogram(command):
        switcher = {
            'update': Update.run,
        }
        return switcher[command]

    if MenuConfig.args.command is not None:
        Tempfolder.init()
        get_subprogram(MenuConfig.args.command)()
    else:
        print('call with -h to see how to run', file=stderr)

if __name__ == '__main__':
    main()
    print('Bye o/')
