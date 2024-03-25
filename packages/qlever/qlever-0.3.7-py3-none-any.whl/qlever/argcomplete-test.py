#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse
import argcomplete
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--foo', required=True, help='foo help')
    comp_line = os.getenv('COMP_LINE', '[not in AC mode]')
    print('COMP_LINE: %s' % comp_line, file=sys.stderr)
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    print(args.foo)

if __name__ == '__main__':
    main()
