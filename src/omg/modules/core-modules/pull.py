from omg.core.tui.components import (REPOSITORY_DOES_NOT_EXIST_MESSAGE,
                                 REPOSITORY_PULL_MESSAGE,
                                 LOG)
from omg.core.exceptions import (RepositoryDoesNotExistsException,
                             PathDoesNotExistException)
from omg.core.repositories import get_repositories, get_repository, check_repository
from typing import List
import omg.core.git
import argparse
import sys
import os

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg pull',
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
    repositories_to_pull = []

    # all mode
    if args.all:
        if args.tags or args.path or args.repositories_aliases:
            pass # log incompatible arguments error
        else:
            repositories_to_pull = omg.core.repositories.get_repositories()

    # filter mode
    repositories_to_pull = omg.core.repositories.get_repositories()

    if args.path:
        args.path = os.path.abspath(args.path)

        if not os.path.exists(args.path):
            raise PathDoesNotExistException(args.path)

        repositories_to_pull = [repositiory_alias for repositiory_alias in repositories_to_pull if args.path in get_repository(repositiory_alias)["path"]]

    if args.tags:
        repositories_to_pull = [repository_alias for repository_alias in repositories_to_pull if get_repository(repository_alias)["tags"] and args.tags in get_repository(repository_alias)["tags"]]


    # alias mode
    if args.repositories_aliases:
        for repository_alias in args.repositories_aliases:
            if not omg.core.repositories.check_repository(repository_alias):
                raise RepositoryDoesNotExistsException(REPOSITORY_DOES_NOT_EXIST_MESSAGE(repository_alias))

        repositories_to_pull = args.repositories_aliases

    # actual pulling
    for repository_alias in repositories_to_pull:
        repository = get_repository(repository_alias)

        omg.core.tui.components.LOG(REPOSITORY_PULL_MESSAGE(repository_alias,repository["origin"]))
        omg.core.git.exec("pull",repository["path"])
        