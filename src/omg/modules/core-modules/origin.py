from omg.core.tui.components import REPOSITORY_DOES_NOT_EXIST_MESSAGE
from omg.core.exceptions import RepositoryDoesNotExistsException
import omg.core.repositories
from typing import List
import omg.core.config
import argparse
import sys
import os

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg origin',
                        description="omg rm allows you to show/open the origin of a specific git repository.",
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("repository_alias",help="select the repository by its alias", nargs="?", type=str,default=".")
    parser.add_argument("-s","--show",help="only show the origin in the terminal, without opening it",action="store_true")

    # parse argv
    args = parser.parse_args(argv)

    # fetch config
    prefered_web_browser = omg.core.config.get_config("prefered-web_browser")
    
    repository = omg.core.repositories.get_repository_from_proxy(args.repository_alias)
    if repository:
        origin = repository["origin"]
        if args.show:
            print(origin)
        else:
            os.system(f"{prefered_web_browser} '{origin}'")
    else:
        raise RepositoryDoesNotExistsException(REPOSITORY_DOES_NOT_EXIST_MESSAGE(args.repository_alias))