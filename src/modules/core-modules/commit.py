from core.tui.components import (
                                LOG,
                                LOG_ERROR,
                                LOG_WARNING,
                                SYSTEM_CALL_ERROR_MESSAGE,
                                REPOSITORY_DOES_NOT_EXIST_MESSAGE)
from core.tui.colors import blue,green,yellow,red
import core.repositories
from typing import List
import core.git
import argparse
import sys
import os

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg-commit',
                        description='omg commit allows you to commit changes to a repository referenced by its alias.',
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("repository_alias",help="alias of the target repository",type=str,default=".")
    parser.add_argument("commit_commands",help="the arguments, options of the commit command",nargs="*",type=str)

    # parse argv
    args = parser.parse_args(argv[:1])
    commit_commands = argv[1:]

    # formatting the arguments 
    for i in range(len(commit_commands)):
        if " " in commit_commands[i]:
            commit_commands[i] = f'"{commit_commands[i]}"'

    commit_commands = "commit " + " ".join(commit_commands)

    # fetching the repository's path
    repository_path = core.repositories.check_repository(args.repository_alias)

    # actual git call
    if repository_path:
        returned_code,_ = core.git.exec(commit_commands,repository_path)
    else:
        LOG_ERROR(REPOSITORY_DOES_NOT_EXIST_MESSAGE(args.repository_alias))
        sys.exit(1)
