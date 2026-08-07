import omg.core.repositories
from omg.modules import list_modules
from typing import List
import argparse
import sys

# modules that accept repository aliases as positional arguments
REPOSITORY_MODULES = {"cd", "commit", "edit", "origin", "icon", "rm", "pull", "run", "legacy", "rename", "tag"}
# modules that accept multiple repository aliases (completion beyond the 2nd word)
MULTI_REPOSITORY_MODULES = {"rm", "pull"}

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg autocomplete',
                        description="omg autocomplete handles omg's auto-completion system",
                        epilog="See 'omg --help' to get further help",
                        add_help=False)

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
    
    # parse argv (parse_known_args to ignore flags passed through from the command line)
    args, _ = parser.parse_known_args(argv)

    if not args.COMP_CWORD.isdigit():
        sys.exit(1)
    
    COMP_CWORD = int(args.COMP_CWORD)
    COMP_WORDS = args.COMP_WORDS

    modules = list_modules()
    repositories = omg.core.repositories.get_repositories()

    if COMP_CWORD == 1:
        print(" ".join(modules))
    elif COMP_CWORD == 2:
        module = COMP_WORDS[1] if len(COMP_WORDS) > 1 else ""
        if module == "help":
            print(" ".join(modules))
        elif module in REPOSITORY_MODULES:
            print(" ".join(repositories.keys()))
    elif COMP_CWORD >= 3:
        module = COMP_WORDS[1] if len(COMP_WORDS) > 1 else ""
        if module == "help":
            print(" ".join(modules))
        elif module in MULTI_REPOSITORY_MODULES:
            print(" ".join(repositories.keys()))

