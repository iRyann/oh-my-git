from core.tui.components import (
                                LOG,
                                LOG_WARNING)
from core.tui.colors import blue,green,yellow
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
    parser.add_argument("-t","--tags",help="filters the repositories by tags",nargs="*",type=str)

    # parse argv
    args = parser.parse_args(argv)
    
    # fetch repositories data
    repositories = core.repositories.get_repositories()
    repositories_names = list(repositories.keys())

    if args.tags:
        repositories_names = [repository_name for repository_name in repositories_names if repositories[repository_name]["tags"] and args.tags in repositories[repository_name]["tags"]]

    # init buffer
    buffer = ""

    # format output -> inline
    if args.inline:
        for repository_name in repositories_names:
            tags =  "" if repositories[repository_name]["tags"] == None else f'\n\ttags: {" ".join(repositories[repository_name]["tags"])}'
            buffer += f'{blue(repository_name)}\n\torigin: {repositories[repository_name]["origin"]}\n\tpath: {repositories[repository_name]["path"]}\n\tauthor: {repositories[repository_name]["author"]}{tags}\n'

    # format output -> ls style                
    else:
        buffer = " \t".join(repositories_names)

    print(buffer)
    LOG(f"Displaying {len(repositories_names)} repositories")
