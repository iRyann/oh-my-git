from core.tui.components import (
                                LOG,
                                LOG_WARNING)
from core.tui.colors import blue,green
import core.repositories
from typing import List
import argparse
import sys

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg-list',
                        description='omg list allows you to list all the repositories registered in omg',
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("-l","--inline",help="display the repositories inline, with minimal informations",action="store_true")
    parser.add_argument("-t","--tags",help="filters the repositories by tags",type=str)

    # parse argv
    args = parser.parse_args(argv)
    
    # fetch repositories data
    repositories = core.repositories.get_repositories()
    repositories_names = list(repositories.keys())

    # init buffer
    buffer = ""

    # format output -> inline
    if args.inline:
        for repository_name in repositories_names:
            tags =  [] if repositories[repository_name]["tags"] == None else repositories[repository_name]["tags"]
            buffer += f'{blue(repository_name)} {repositories[repository_name]["origin"]} {blue("->")} {repositories[repository_name]["path"]} {green(" ".join(tags))}\n'

    # format output -> ls style                
    else:
        pass

    print(buffer)
