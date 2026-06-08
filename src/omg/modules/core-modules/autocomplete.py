import omg.core.repositories
from omg.modules import list_modules
from typing import List
import argparse
import sys

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg autocomplete',
                        description="omg autocomplete handles omg's auto-completion system",
                        epilog="See 'omg --help' to get further help")

    # add arguments

    parser.add_argument("COMP_CWORD",
                        help="index of the current word in the word list",
                        type=str,
                        default=None)

    parser.add_argument("COMP_WORDS",
                        help="list of words",
                        nargs="*",
                        type=str,
                        default=None)
    
    # parse argv
    args = parser.parse_args(argv)

    if not args.COMP_CWORD.isdigit():
        sys.exit(1)
    
    COMP_CWORD = int(args.COMP_CWORD)

    if COMP_CWORD == 1:
        print(" ".join(list_modules()))
    else:
        print(" ".join(omg.core.repositories.get_repositories()))