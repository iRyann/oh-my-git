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

def entrypoint(argv : List[str])->None:
    # init parser
    parser = argparse.ArgumentParser(
                        prog='omg tag',
                        description='omg tag allows you to add or remove tags on a repository.',
                        epilog="See 'omg --help' to get further help")

    # add arguments
    parser.add_argument("repository_alias",help="alias of the target repository",type=str)
    parser.add_argument("--add",help="add tags to the repository",nargs="+",type=str)
    parser.add_argument("--remove",help="remove tags from the repository",nargs="+",type=str)

    # parse argv
    args = parser.parse_args(argv)

    if not args.add and not args.remove:
        LOG_ERROR("You must specify at least one of --add or --remove")
        sys.exit(1)

    if not omg.core.repositories.check_repository(args.repository_alias):
        raise RepositoryDoesNotExistsException(REPOSITORY_DOES_NOT_EXIST_MESSAGE(args.repository_alias))

    repository = omg.core.repositories.get_repository(args.repository_alias)

    if repository["tags"] is None:
        repository["tags"] = []

    if args.add:
        for tag in args.add:
            if tag not in repository["tags"]:
                repository["tags"].append(tag)
                LOG(f"Added tag '{green(tag)}' to '{blue(args.repository_alias)}'")
            else:
                LOG_WARNING(f"Tag '{yellow(tag)}' already exists on '{blue(args.repository_alias)}'")

    if args.remove:
        for tag in args.remove:
            if tag in repository["tags"]:
                repository["tags"].remove(tag)
                LOG(f"Removed tag '{red(tag)}' from '{blue(args.repository_alias)}'")
            else:
                LOG_WARNING(f"Tag '{yellow(tag)}' does not exist on '{blue(args.repository_alias)}'")

    omg.core.repositories.save_repositories()
