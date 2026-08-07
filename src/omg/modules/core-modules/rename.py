from omg.core.tui.components import (
                                LOG,
                                LOG_ERROR,
                                LOG_WARNING,
                                REPOSITORY_DOES_NOT_EXIST_MESSAGE)
from omg.core.exceptions import RepositoryDoesNotExistsException
import omg.core.repositories
from omg.core.tui.colors import blue,green,yellow,red
from typing import List
import argparse
import sys
import os

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg rename',
                        description='omg rename allows you to rename a repository alias and/or its directory on the file system.',
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("target_alias",help="alias of the repository to rename",type=str)
    parser.add_argument("new_name",help="new alias or directory name",type=str)

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("-d","--directory",help="rename the directory on the file system only",action="store_true")
    mode_group.add_argument("-f","--full",help="rename both the alias and the directory",action="store_true")

    # parse argv
    args = parser.parse_args(argv)

    # check if target repository exists
    if not omg.core.repositories.check_repository(args.target_alias):
        raise RepositoryDoesNotExistsException(REPOSITORY_DOES_NOT_EXIST_MESSAGE(args.target_alias))

    repository = omg.core.repositories.get_repository(args.target_alias)
    repository_path = repository["path"]

    rename_alias = not args.directory  # default or --full
    rename_directory = args.directory or args.full

    # validate alias rename
    if rename_alias:
        if args.new_name in omg.core.repositories.get_repositories():
            LOG_ERROR(f"A repository already exists with the alias '{args.new_name}'")
            sys.exit(1)

    # validate and perform directory rename
    new_path = None
    if rename_directory:
        parent_dir = os.path.dirname(repository_path)
        new_path = os.path.join(parent_dir, args.new_name)

        if os.path.exists(new_path):
            LOG_ERROR(f"A directory already exists at '{new_path}'")
            sys.exit(1)

        os.rename(repository_path, new_path)

    # perform alias rename
    if rename_alias:
        repository_data = omg.core.repositories.get_repository(args.target_alias)
        if rename_directory:
            repository_data["path"] = new_path

        omg.core.repositories.REPOSITORIES[args.new_name] = repository_data
        del omg.core.repositories.REPOSITORIES[args.target_alias]
    elif rename_directory:
        omg.core.repositories.update_repository(args.target_alias, {"path": new_path})

    omg.core.repositories.save_repositories()

    if rename_alias and rename_directory:
        LOG(f"Renamed repository '{red(args.target_alias)}' to '{green(args.new_name)}' and directory to '{green(new_path)}'")
    elif rename_alias:
        LOG(f"Renamed repository '{red(args.target_alias)}' to '{green(args.new_name)}'")
    else:
        LOG(f"Renamed directory of '{blue(args.target_alias)}' to '{green(new_path)}'")
