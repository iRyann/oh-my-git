from core.tui.components import (
                                LOG,
                                LOG_ERROR,
                                LOG_WARNING,
                                REPOSITORY_DOES_NOT_EXIST_MESSAGE)
from core.tui.colors import blue,green,yellow,red
import core.repositories
from typing import List
import argparse
import sys
import os

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg rm',
                        description='omg rm allows you to remove repositories registered in omg.\
                                    By default, repositories are only removed from the omg resister',
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("repositories_names",help="remove repositories by name",type=str,nargs="*",default=None)
    parser.add_argument("-H","--hard",help="remove repositories from your file system",action="store_true")
    parser.add_argument("-p","--path",help="remove the repositories lcoated in a path and its sub directories",type=str)
    parser.add_argument("-a","--author",help="remove the repositories from an certain author",type=str)
    parser.add_argument("-t","--tags",help="remove the repositories with a certain combination of tags",nargs="*",type=str)

    # parse argv
    args = parser.parse_args(argv)
    
    # fetch repositories data
    repositories = core.repositories.get_repositories()
    repositories_names = list(repositories.keys())

    # applying filters

    if args.repositories_names:
        repositories_names = []

        # filtering and checking if repository exists
        for repository_name in args.repositories_names:
            if not core.repositories.check_repository(repository_name):
                LOG_ERROR(REPOSITORY_DOES_NOT_EXIST_MESSAGE(repository_name))
                sys.exit(1)
            else:
                repositories_names.append(repository_name)

    if args.tags:
        repositories_names = [repository_name for repository_name in repositories_names if repositories[repository_name]["tags"] and args.tags in repositories[repository_name]["tags"]]

    if args.author:
        repositories_names = [repository_name for repository_name in repositories_names if args.author in repositories[repository_name]["author"]]

    if args.path:
        args.path = os.path.realpath(args.path)
        repositories_names = [repository_name for repository_name in repositories_names if args.path in repositories[repository_name]["path"]]

    # format deleted repositories output before deleting
    removed_buffer = ""

    for repository_name in repositories_names:
        removed_buffer += f'{red("- ")}{repositories[repository_name]["path"]} known as {red(repository_name)}\n'

    if repositories_names != []:
        # remove the repositories from the file system
        if args.hard:
            try:
                # warning the user
                number_of_repository_message = f"These {len(repositories_names)} repositories are" if len(repositories_names) > 1 else f"1 repository is"
                LOG_WARNING(f'{number_of_repository_message} about to be removed from the file system')
                remove_candidate_buffer = ""

                # outputing the repos about to be removed
                for repository_name in repositories_names:
                    remove_candidate_buffer += f'{yellow("? ")}{repositories[repository_name]["path"]} known as {yellow(repository_name)}\n'
                
                print(remove_candidate_buffer)

                # processing the users input
                proceed = input("Do you want to proceed ? Y/n : ")
                if proceed == "Y":
                    # actual removal from the file system
                    core.repositories.remove_repositories(repositories_names)
                    core.repositories.forget_repositories(repositories_names)
                else:
                    sys.exit(0)
            except:
                sys.exit(1)          

        # just forgetting about the repositories
        else:
            core.repositories.forget_repositories(repositories_names)

        core.repositories.save_repositories()
        
        # final output
        print(removed_buffer)
        LOG(f'{len(repositories_names)} repositor{"ies" if len(repositories_names) > 1 else "y"} have been removed {"from your file system." if args.hard else "from omg."}')
    
    else:
        # empty matching repository names list
        LOG_WARNING("There are no repositories matching the filters. Unable to proceed.")
