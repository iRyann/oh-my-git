from core.tui.components import REPOSITORY_DOES_NOT_EXIST_MESSAGE,LOG_ERROR
from core.exceptions import RepositoryDoesNotExistsException
import core.repositories
from typing import List
import core.config
import argparse
import sys
import os

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg icon',
                        description="omg icon allows you to append unicode characters after your repository's alias. You can copy and paste icons from here : https://www.amp-what.com/",
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("repository_proxy",help="select the repository by its alias", nargs="?", type=str,default=".")
    parser.add_argument("--add",help="add a new unicode icon",type=str)
    parser.add_argument("--remove",help="A unicode icon",type=str)

    # parse argv
    args = parser.parse_args(argv)

    # fetch config
    repository = core.repositories.get_repository_from_proxy(args.repository_proxy)

    if repository:
        if args.add:
            repository["icons"].append(args.add)
        if args.remove:
            if args.remove in repository["icons"]:
                repository["icons"].remove(args.remove)
            else:
                # looking for the repository alias
                repository_name = next((repository_name
                    for repository_name, repository_candidate in core.repositories.get_repositories().items()
                    if repository_candidate == repository)
                    , None)

                LOG_ERROR(f"The icon '{args.remove}' is not one of the repository '{repository_name}'")
                sys.exit(1)

        core.repositories.save_repositories()

    else:
        raise RepositoryDoesNotExistsException(REPOSITORY_DOES_NOT_EXIST_MESSAGE(args.repository_proxy))