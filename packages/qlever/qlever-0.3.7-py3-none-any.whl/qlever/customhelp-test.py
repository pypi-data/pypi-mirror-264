#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

import argparse
import argcomplete

# class MyHelpFormatter(argparse.HelpFormatter):
#     def _format_action_invocation(self, action):
#         if not action.option_strings:
#             default = self._get_default_metavar_for_positional(action)
#             metavar = getattr(action, 'metavar', default)
#             return metavar
#         else:
#             parts = []
#             if action.nargs == 0:
#                 parts.extend(action.option_strings)
#             else:
#                 default = self._get_default_metavar_for_optional(action)
#                 args_string = self._format_args(action, default)
#                 parts.extend(action.option_strings)
#                 parts[-1] += ' ' + args_string
#             return ', '.join(parts)
# 
class MyHelpAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        parser.print_help()
        parser.print_help()
        parser.exit()

def main():
    parser = argparse.ArgumentParser(description='This is MY script')
    parser.add_argument('--foo', required=True, help='foo help')
    # parser.add_argument('--help', action=MyHelpAction, nargs=0,
    #                     help='this is MY help message')
    # parser.add_argument('--help', action=MyHelpAction, help='show this help message and exit')
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    print(args.foo)

if __name__ == '__main__':
    main()
