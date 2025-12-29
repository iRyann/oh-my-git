from core.tui.components import (
                                LOG,
                                LOG_ERROR,
                                LOG_WARNING,
                                REPOSITORY_DOES_NOT_EXIST_MESSAGE)
from core.tui.colors import blue,green,yellow,red
import core.repositories
from typing import List
import core.config
import argparse
import sys
import os

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg-cd',
                        description="omg rm allows you to open a new shell session which the current working directory is set to the root of a specific git repository.",
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("repository_alias",help="select the repository by its alias",type=str,default=None)

    # parse argv
    args = parser.parse_args(argv)
    
    # fetch repositories data
    repositories = core.repositories.get_repositories()
    repositories_names = list(repositories.keys())

    # fetch config
    prefered_shell = core.config.get_config("prefered-shell")

    if args.repository_alias in repositories_names:
        os.chdir(repositories[args.repository_alias]["path"])
        os.system(prefered_shell)