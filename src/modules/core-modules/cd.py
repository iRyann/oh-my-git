from core.tui.components import REPOSITORY_DOES_NOT_EXIST_MESSAGE
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
                        prog='omg cd',
                        description="omg rm allows you to open a new shell session which the current working directory is set to the root of a specific git repository.",
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("repository_alias",help="select the repository by its alias",type=str,default=None)

    # parse argv
    args = parser.parse_args(argv)

    # fetch config
    prefered_shell = core.config.get_config("prefered-shell")

    if core.repositories.check_repository(args.repository_alias):
        os.chdir(core.repositories.get_repository(args.repository_alias)["path"])
        os.system(prefered_shell)
    else:
        raise RepositoryDoesNotExistsException(REPOSITORY_DOES_NOT_EXIST_MESSAGE(args.repository_alias))