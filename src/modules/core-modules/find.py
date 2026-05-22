from core.tui.components import (
                                LOG,
                                LOG_WARNING,
                                LOG_ERROR)
from core.tui.colors import blue,green
import core.repositories
from typing import List
import core.git
import argparse
import sys
import os

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg find',
                        description='omg list allows you to find repositories on your system',
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("start_paths",
                        help="choose the starting paths of the research",
                        nargs="*",type=str,
                        default=["."])

    # parse argv
    args = parser.parse_args(argv)

    # get repositories object
    repositories = core.repositories.get_repositories()

    # search repositories
    try:
        pipe = os.popen(f'find {" ".join(args.start_paths)} | grep /.git$',"r")
        found_repositories = pipe._stream.read().split("\n")[:-1]
        found_repositories = [os.path.realpath(os.path.split(found_repository)[0]) for found_repository in found_repositories]
        error_code = pipe.close()
    except:
        LOG_ERROR("An error occured while requesting the system to search for the repositories\nMake sure you have 'find' and 'grep' installed on your system")
        sys.exit(1)

    if error_code:
        LOG_ERROR("A system call went wrong")
        sys.exit(1)

    repositories_names = list(repositories.keys())
    repositories_path = [repository["path"] for repository in repositories.values()]
    new_repositories_path = [repository_path for repository_path in found_repositories if repository_path not in repositories_path]
    already_known_repositories_path = [repository_path for repository_path in found_repositories if repository_path not in new_repositories_path]
    new_aliases = [os.path.split(repository_path)[1] for repository_path in new_repositories_path]
    
    # check if the aliases are all available
    for i in range(len(new_aliases)):
        counter = 1
        original_alias = new_aliases[i]

        while new_aliases[i] in repositories_names:
            new_aliases[i] = original_alias + str(counter)
            counter += 1
        
        repositories_names.append(new_aliases[i])
            
    # actually registering the new repositories
    for i in range(len(new_repositories_path)):
        repository_data = {"path" : new_repositories_path[i], "tags" : None, "icons": []}
        repository_data["author"] = core.git.get_author(new_repositories_path[i])
        repository_data["origin"] = core.git.get_origin(new_repositories_path[i])
        core.repositories.add_repository(new_aliases[i],repository_data)

    core.repositories.save_repositories()

    new_repositories_display = [f"{data[0]} as {green(data[1])}" for data in zip(new_repositories_path,new_aliases)]

    print("\n".join(already_known_repositories_path))
    print(green("+ ")*(new_repositories_path != []) + f'\n{green("+")} '.join(new_repositories_display) + "\n")

    LOG(f'Found {len(found_repositories)} {"repositories" if len(found_repositories) > 1 else "repository"} including {green(str(len(new_repositories_path)) + " new")} {"repositories" if len(new_repositories_path) > 1 else "repository"}')
