from core.tui.components import (REPOSITORY_DOES_NOT_EXIST_MESSAGE,
                                 REPOSITORY_PULL_MESSAGE,
                                 LOG)
from core.exceptions import RepositoryDoesNotExistsException
import core.repositories
from typing import List
import core.git
import argparse
import sys
import os


def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg-pull',
                        description='omg to pull changes, for a specific set of repositories, from their respective origins',
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument(
        "repositories_aliases",
        help="select repositories by their aliases",
        type=str,
        nargs="*",
        default=None
    )

    parser.add_argument(
        "-t",
        "--tags",
        help="select repositories by tags",
        type=str,
        nargs="*",
        default=None
    )

    parser.add_argument(
        "-p",
        "--path",
        help="select repositories within a path",
        type=str,
        default=None
    )

    parser.add_argument(
        "-A",
        "--all",
        help="select all repositories",
        action="store_true"
    )


    # parse argv
    args = parser.parse_args(argv)

    # all mode
    if args.all:
        if args.tags or args.path or args.repositories_aliases:
            pass # logerror
        else:
            pass # all

    # filter mode

    # alias mode

    for repository_alias in args.repositories_aliases:
        if not core.repositories.check_repository(repository_alias):
            raise RepositoryDoesNotExistsException(REPOSITORY_DOES_NOT_EXIST_MESSAGE(repository_alias))
    
    for repository_alias in args.repositories_aliases:
        repository = core.repositories.get_repository(repository_alias)

        core.tui.components.LOG(REPOSITORY_PULL_MESSAGE(repository_alias,repository["origin"]))
        core.git.exec("pull",repository["path"])
        