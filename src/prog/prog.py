#!/usr/bin/env python
"""
    python prog.py

    TODO: Add usage information here.
"""
import sys
# TODO: Uncomment or add imports here.
#import os
#import re
#import time
#import subprocess
from argparse import ArgumentParser

def execute_prog(par1):
    """ TODO: Add docstring here. """
    # TODO: Add or delete code here.
    # Dump all passed argument values.
    print 'par1 = {0}'.format(repr(par1))
    return 0

# Start of main program.
def main(argv=None):
    # Initialize the command line parser.
    parser = ArgumentParser(description='TODO: Text to display before the argument help.',
                            epilog='Copyright (c) 2018 TODO: your-name-here.',
                            add_help=True,
                            argument_default=None, # Global argument default
                            usage=__doc__)
    parser.add_argument(action='store', dest='par1', help='TODO:')
    # Parse the command line.
    arguments = parser.parse_args(args=argv)
    par1 = arguments.par1
    status = 0
    try:
        execute_prog(par1)
    except ValueError as value_error:
        print value_error
        status = -1
    except EnvironmentError as environment_error:
        print environment_error
        status = -1
    return status

if __name__ == "__main__":
    sys.exit(main())
